import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data.dataloader import default_collate
from torch.utils.data.sampler import SubsetRandomSampler, SequentialSampler

from typing import Iterator, Optional, Sequence, List, TypeVar, Generic, Sized

class StaticSampler:
    r"""Samples elements sequentially, always in the same order.

    Arguments:
        data_source (Dataset): dataset to sample from
    """
    order: List[int]

    def __init__(self, order):
        self.order = order

    def __iter__(self):
        return iter(self.order.tolist())

    def __len__(self) -> int:
        return len(self.order)

class BaseDataLoader(DataLoader):
    """
    Base class for all data loaders
    """
    def __init__(self, dataset, batch_size, shuffle, validation_split, num_workers, collate_fn=default_collate):
        self.validation_split = validation_split
        self.shuffle = shuffle
        self.dataset = dataset

        self.batch_idx = 0
        self.n_samples = len(dataset)

        self.init_kwargs = {
            'dataset': dataset,
            'batch_size': batch_size,
            'shuffle': False, # mutually exclusive with sampler
            'collate_fn': collate_fn,
            'num_workers': num_workers
        }

        self.sampler, self.valid_sampler = self._split_sampler(self.validation_split)      

        super().__init__(sampler=self.sampler, **self.init_kwargs)

    def _split_sampler(self, split):
        if split == 0.0:
            return None, None

        idx_full = np.arange(self.n_samples)

        np.random.seed(0)
        np.random.shuffle(idx_full)

        if isinstance(split, int):
            assert split > 0
            assert split < self.n_samples, "validation set size is configured to be larger than entire dataset."
            len_valid = split
        else:
            len_valid = int(self.n_samples * split)

        valid_idx = idx_full[0:len_valid]
        train_idx = np.delete(idx_full, np.arange(0, len_valid))

        self.unshuffle_idx = np.zeros(self.n_samples, dtype=int)
        self.unshuffle_idx[np.concatenate((valid_idx, train_idx))] = np.arange(0, self.n_samples, dtype=int)

        self.unshuffled_train = DataLoader(sampler=StaticSampler(train_idx), **self.init_kwargs)
        self.unshuffled_valid = DataLoader(sampler=StaticSampler(valid_idx), **self.init_kwargs)

        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)
        
        self.n_samples = len(train_idx)

        return train_sampler, valid_sampler

    def split_validation(self):
        if self.valid_sampler is None:
            return None
        else:
            return DataLoader(sampler=self.valid_sampler, **self.init_kwargs)
