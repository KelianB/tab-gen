from random import random
import numpy as np

# The maximum proportion of columns to cut out of the image
MAX_CUTOUT = 0.4

class RandomColumnCutout():
    def __init__(self):
        pass

    def __call__(self, sample):
        image, target = sample["image"], sample["target"]

        proportion = np.random.rand() * MAX_CUTOUT
        n_cols = int(image.shape[2] * proportion)
        first_col = np.random.randint(0, image.shape[2] - n_cols)
        
        image[:, :, first_col : first_col + n_cols] = 255
        
        return {"image": image, "target": target}

    def __repr__(self):
        repr = f"{self.__class__.__name__  }"
        return repr
