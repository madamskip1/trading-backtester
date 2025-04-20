from typing import Any

import numpy as np

from stock_backtesting.backtest import BacktestingDataType


def load_csv(file_path: str) -> np.ndarray[Any, np.dtype[Any]]:
    return np.genfromtxt(
        file_path,
        delimiter=",",
        skip_header=1,
        dtype=BacktestingDataType,
        usecols=(1, 2, 3, 4),
    )
