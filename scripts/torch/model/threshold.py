import pickle
import torch
import pathlib
from typing import Optional
from skimage.filters.thresholding import threshold_otsu


class Threshold:
    def __init__(self, threshold: Optional[float] = None):
        self.threshold = threshold

    @classmethod
    def load(cls, filepath):
        with open(filepath, "rb") as f:
            threshold = pickle.load(f)

        if not isinstance(threshold, cls):
            raise Exception("Invalid threshold file")
        return threshold

    def save(self, filepath: pathlib.Path):
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    def fit(self, x: torch.Tensor):
        self.threshold = threshold_otsu(x.cpu().numpy())

    def fit_transform(self, x: torch.Tensor):
        self.fit(x)
        return self(x)

    def transform(self, x: torch.Tensor):
        return self(x)

    def __call__(self, x: torch.Tensor):
        if self.threshold is None:
            raise Exception("Threshold not fitted")
        return x > self.threshold
