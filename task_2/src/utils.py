import numpy as np
from pathlib import Path

def load_data(dirname: str) -> np.ndarray:
    files_in_dirname = sorted(Path(dirname).glob("*.csv"))
    if not files_in_dirname:
        raise FileNotFoundError(f"No .csv files in '{dirname}'")
    # wczytujemy i laczymy wszystkie dane
    data = np.vstack([np.loadtxt(file, delimiter=',') for file in files_in_dirname])

    return data

""" standaryzacja Z-score"""
def scale_data(train_data: np.ndarray, test_data: np.ndarray) -> (np.ndarray, np.ndarray):
    mean = np.mean(train_data, axis=0)
    std = np.std(train_data, axis=0)

    # zeby uniknac dzielenia przez 0
    std[std == 0] = 1.0

    train_data_scaled = (train_data - mean) / std
    test_data_scaled = (test_data - mean) / std

    return train_data_scaled, test_data_scaled
