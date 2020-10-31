import torch.nn.functional as F
import torch
import numpy as np

# def nll_loss(output, target):
    # return F.nll_loss(output, target)

# Very small value added to the outputs to avoid log(0)
eps = 1e-15

def multi_cross_entropy_loss(output, target):
    loss = (target * torch.log(output + eps)).sum(2) # sum for all frets
    loss = loss.sum(1) # for all strings
    loss = -loss.mean() # for the entire batch
    return loss


"""
m = 1e-1
M = 1-m

l = multi_cross_entropy_loss(torch.from_numpy(np.array([
    [
        [M, m, m],
        [m, M, m],
        [m, m, M],
    ],
])), torch.from_numpy(np.array([
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ],
])))
print(l)
"""