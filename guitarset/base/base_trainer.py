import torch
from abc import abstractmethod
from numpy import inf
from logger import TensorboardWriter
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import re

class BaseTrainer:
    """
    Base class for all trainers
    """
    def __init__(self, model, criterion, metric_ftns, optimizer, config):
        self.config = config
        self.logger = config.get_logger('trainer', config['trainer']['verbosity'])

        # setup GPU device if available, move model into configured device
        self.device, device_ids = self._prepare_device(config['n_gpu'])
        self.model = model.to(self.device)
        if len(device_ids) > 1:
            self.model = torch.nn.DataParallel(model, device_ids=device_ids)

        self.criterion = criterion
        self.metric_ftns = metric_ftns
        self.optimizer = optimizer

        cfg_trainer = config['trainer']
        self.epochs = cfg_trainer['epochs']
        self.save_period = cfg_trainer['save_period']
        self.monitor = cfg_trainer.get('monitor', 'off')

        # configuration to monitor model performance and save best
        if self.monitor == 'off':
            self.mnt_mode = 'off'
            self.mnt_best = 0
        else:
            self.mnt_mode, self.mnt_metric = self.monitor.split()
            assert self.mnt_mode in ['min', 'max']

            self.mnt_best = inf if self.mnt_mode == 'min' else -inf
            self.early_stop = cfg_trainer.get('early_stop', inf)

        self.start_epoch = 1

        self.checkpoint_dir = config.save_dir

        # setup visualization writer instances                
        self.writer_train = TensorboardWriter(config.log_dir_train, self.logger, cfg_trainer['tensorboard'])
        self.writer_val =   TensorboardWriter(config.log_dir_val, self.logger, cfg_trainer['tensorboard'])

        if config.resume is not None:
            self._resume_checkpoint(config.resume)

    @abstractmethod
    def _train_epoch(self, epoch):
        """
        Training logic for an epoch

        :param epoch: Current epoch number
        """
        raise NotImplementedError

    def train(self):
        """
        Full training logic
        """
        not_improved_count = 0
        for epoch in range(self.start_epoch, self.epochs + 1):
            result = self._train_epoch(epoch)

            # save logged informations into log dict
            log = {'epoch': epoch}
            log.update(result)

            # print logged informations to the screen
            for key, value in log.items():
                self.logger.info('    {:15s}: {}'.format(str(key), value))

            # evaluate model performance according to configured metric, save best checkpoint as model_best
            best = False
            if self.mnt_mode != 'off':
                try:
                    # check whether model performance improved or not, according to specified metric(mnt_metric)
                    improved = (self.mnt_mode == 'min' and log[self.mnt_metric] <= self.mnt_best) or \
                               (self.mnt_mode == 'max' and log[self.mnt_metric] >= self.mnt_best)
                except KeyError:
                    self.logger.warning("Warning: Metric '{}' is not found. "
                                        "Model performance monitoring is disabled.".format(self.mnt_metric))
                    self.mnt_mode = 'off'
                    improved = False

                if improved:
                    self.mnt_best = log[self.mnt_metric]
                    not_improved_count = 0
                    best = True
                else:
                    not_improved_count += 1

                if not_improved_count > self.early_stop:
                    self.logger.info("Validation performance didn\'t improve for {} epochs. "
                                     "Training stops.".format(self.early_stop))
                    break

            if epoch % self.save_period == 0:
                self._save_checkpoint(epoch, save_best=best)

    def _prepare_device(self, n_gpu_use):
        """
        setup GPU device if available, move model into configured device
        """
        n_gpu = torch.cuda.device_count()
        if n_gpu_use > 0 and n_gpu == 0:
            self.logger.warning("Warning: There\'s no GPU available on this machine,"
                                "training will be performed on CPU.")
            n_gpu_use = 0
        if n_gpu_use > n_gpu:
            self.logger.warning("Warning: The number of GPU\'s configured to use is {}, but only {} are available "
                                "on this machine.".format(n_gpu_use, n_gpu))
            n_gpu_use = n_gpu
        device = torch.device('cuda:0' if n_gpu_use > 0 else 'cpu')
        list_ids = list(range(n_gpu_use))
        return device, list_ids

    def _save_checkpoint(self, epoch, save_best=False):
        """
        Saving checkpoints

        :param epoch: current epoch number
        :param log: logging information of the epoch
        :param save_best: if True, rename the saved checkpoint to 'model_best.pth'
        """
        arch = type(self.model).__name__
        state = {
            'arch': arch,
            'epoch': epoch,
            'state_dict': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'monitor_best': self.mnt_best,
            'config': self.config
        }
        filename = str(self.checkpoint_dir / 'checkpoint-epoch{}.pth'.format(epoch))
        torch.save(state, filename)
        self.logger.info("Saving checkpoint: {} ...".format(filename))
        if save_best:
            # Compute global metrics and merge them with the checkpoint
            self.logger.info("Computing metrics...")
            self.save_metrics()

            best_path = str(self.checkpoint_dir / 'model_best.pth')
            torch.save(state, best_path)
            self.logger.info("Saving current best: model_best.pth ...")

    def _resume_checkpoint(self, resume_path):
        """
        Resume from saved checkpoints

        :param resume_path: Checkpoint path to be resumed
        """
        resume_path = str(resume_path)
        self.logger.info("Loading checkpoint: {} ...".format(resume_path))
        checkpoint = torch.load(resume_path)
        self.start_epoch = checkpoint['epoch'] + 1
        self.mnt_best = checkpoint['monitor_best']

        # load architecture params from checkpoint.
        if checkpoint['config']['arch'] != self.config['arch']:
            self.logger.warning("Warning: Architecture configuration given in config file is different from that of "
                                "checkpoint. This may yield an exception while state_dict is being loaded.")
        self.model.load_state_dict(checkpoint['state_dict'])

        # load optimizer state from checkpoint only when optimizer type is not changed.
        if checkpoint['config']['optimizer']['type'] != self.config['optimizer']['type']:
            self.logger.warning("Warning: Optimizer type given in config file is different from that of checkpoint. "
                                "Optimizer parameters not being resumed.")
        else:
            self.optimizer.load_state_dict(checkpoint['optimizer'])

        self.logger.info("Checkpoint loaded. Resume training from epoch {}".format(self.start_epoch))

    def save_metrics(self):
        labels = list(range(0,19))
        filename_metrics = str(self.checkpoint_dir / 'metrics_best.csv')
        filename_outputs = str(self.checkpoint_dir / 'outputs_best.csv')

        y_true_val = None
        y_pred_val = None
        y_true_train = None
        y_pred_train = None

        data_train = self.data_loader.unshuffled_train
        data_valid = self.data_loader.unshuffled_valid

        # Forward pass the validation set
        print("Forward pass - validation set")
        for batch_idx, (data, target) in enumerate(data_valid):
            data = data.to(self.device)
            pred = self.model(data).cpu().detach()         

            # One-hot decoding from shape (batch_size, 6, 19) to shape (batch_size, 6)
            target = np.argmax(target, axis=2)
            pred = np.argmax(pred, axis=2)

            # Store
            y_true_val = target if batch_idx == 0 else np.concatenate((y_true_val, target))
            y_pred_val = pred   if batch_idx == 0 else np.concatenate((y_pred_val, pred))

        # Forward pass the training set
        print("Forward pass - training set")
        for batch_idx, (data, target) in enumerate(data_train):
            data = data.to(self.device)
            pred = self.model(data).cpu().detach()         

            # One-hot decoding from shape (batch_size, 6, 19) to shape (batch_size, 6)
            target = np.argmax(target, axis=2)
            pred = np.argmax(pred, axis=2)

            # Store
            y_true_train = target if batch_idx == 0 else np.concatenate((y_true_train, target))
            y_pred_train = pred   if batch_idx == 0 else np.concatenate((y_pred_train, pred))

        # shape of y_true and y_pred: (n_samples, 6)
        
        print("Calculating confusion matrices")
        csv_rows = get_csv_confusion_matrices(y_true_train, y_pred_train, labels)
  
        print("Calculating classification reports")
        csv_rows += [] + get_csv_cls_reports(y_true_train, y_pred_train, labels)

        import csv

        # Save outputs to .csv
        n_val = y_pred_val.shape[0]
        with open(filename_outputs, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
  
            true_val =   y_true_val.tolist()
            true_train = y_true_train.tolist()
            pred_val =   y_pred_val.tolist()
            pred_train = y_pred_train.tolist()
            n_val = len(pred_val)
            rows = [["val"]   + cols + [sum(true_val[i])]   for i,cols in enumerate(pred_val)] \
                 + [["train"] + cols + [sum(true_train[i])] for i,cols in enumerate(pred_train)]
            ordered_rows = np.array(rows)[self.data_loader.unshuffle_idx].tolist()
            writer.writerows(ordered_rows)

        # Save metrics to .csv
        with open(filename_metrics, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            writer.writerows(csv_rows)
    

def get_csv_confusion_matrices(y_true, y_pred, labels):
    csv_rows = []
    for i in range(6):
        csv_rows.append(["Confusion Matrix - String #" + str(i+1)])
        matrix = confusion_matrix(y_true[:,i], y_pred[:,i], labels=labels)
        csv_rows.append([""]+list(range(len(matrix))))
        for j in range(len(matrix)):
            csv_rows.append([j] + matrix[j].tolist())
    return csv_rows

def get_csv_cls_reports(y_true, y_pred, labels):
    csv_rows = []
    for i in range(6):
        csv_rows.append(["Classification report - String #" + str(i+1)])
        report = classification_report(y_true[:,i], y_pred[:,i], labels=labels)
        report = re.sub(r"\n\n", r"\n", report)
        report = re.sub(r"^'\s+", "", report)
        report = re.sub(r"'", ",", report)
        report = re.sub(r"\n\s{2,}", r"\n", report)
        report = re.sub(r"\s{2,}", ",", report)
                    
        for k,x in enumerate(report.split("\n")[:-1]):
            cols = ([""] if k == -1 else []) + x.split(",")
            csv_rows.append(cols)
    return csv_rows
