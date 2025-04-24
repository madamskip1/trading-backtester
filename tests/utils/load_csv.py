from typing import Any

import numpy as np

from stock_backtesting.data import DATA_TYPE


def load_csv(file_path: str) -> np.ndarray[Any, np.dtype[Any]]:
    return np.genfromtxt(
        file_path,
        delimiter=",",
        skip_header=1,
        dtype=DATA_TYPE,
        usecols=(1, 2, 3, 4),
    )
