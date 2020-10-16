import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import cv2
import os

class GuitarSetDataset(Dataset):
    """GuitarSet dataset."""

    def __init__(self, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.root_dir = root_dir
        self.transform = transform
        self.csv = pd.read_csv(os.path.join(root_dir, "index.csv"), delimiter=";")
        
    def __len__(self):
        return len(self.csv)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        # Read image
        img_name = os.path.join(self.root_dir, self.csv.iloc[idx, 0])
        image = cv2.imread(img_name + ".png")

        # Parse and one-hot-encode the annotation
        notes = np.fromstring(self.csv.iloc[idx, 1], dtype=np.int8, sep=" ")
        one_hot_encoded = np.zeros((notes.size, 19)) # 6x19 matrix
        one_hot_encoded[np.arange(notes.size), notes] = 1

        sample = {'image': image, 'guitar_notes': one_hot_encoded}

        if self.transform:
            sample = self.transform(sample)

        return sample