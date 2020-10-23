import torch

def accuracy(output, target):
    with torch.no_grad():
        predictions = torch.argmax(output, dim=2)
        correct_idx = torch.argmax(target, dim=2)
        assert predictions.shape[0] == len(target)
        correct = torch.sum(predictions == correct_idx).item() / 6
    return correct / len(target)

def top_k_acc(output, target, k=3):
    with torch.no_grad():ct_idx = 
        predictions = torch.topk(output, k, dim=2)[1]
        correct_idx = torch.argmax(target, dim=2)
        assert predictions.shape[0] == len(target)
        correct = sum(torch.sum(predictions[:, :, i] == correct_idx).item() / 6 for i in range(k))
    return correct / len(target)
