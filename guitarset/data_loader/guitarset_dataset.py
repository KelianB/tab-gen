import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
import cv2
import os

INDEX_CSV = "index0.csv"

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
        self.csv = pd.read_csv(os.path.join(root_dir, INDEX_CSV), delimiter=";", header=None)

    def __len__(self):
        return len(self.csv)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        # Read image
        img_file = os.path.join(self.root_dir, self.csv.iloc[idx, 0])
        img_cv2 = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)

        # Resize & convert
        # img_cv2 = cv2.resize(img_cv2, (160, 120), interpolation=cv2.INTER_CUBIC)
        image = torch.from_numpy(np.array([img_cv2])).float()
         
        # Parse and one-hot-encode the annotation
        notes = np.fromstring(self.csv.iloc[idx, 1], dtype=np.int64, sep=" ")
        target = np.zeros((notes.size, 19)) # 6x19 matrix
        target[np.arange(notes.size), notes] = 1

        if self.transform:
          transformed = self.transform({"image": image, "target": target})
          image, target = transformed["image"], transformed["target"]

        return image, target