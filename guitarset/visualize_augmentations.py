import argparse
import torch
import numpy as np
from data_loader.data_loaders import GuitarSetDataLoader
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data_dir = "data/guitar-set/"
    data_loader = GuitarSetDataLoader(data_dir, batch_size=16, shuffle=False, validation_split=0.0, num_workers=1, training=True)
    
    i = 0
    image, target = data_loader.dataset.__getitem__(i)
    img = image[0].numpy()
    plt.imshow(img, cmap="gray")
    
    plt.show()