from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np

from stock_backtesting.data import Data


class Indicator(ABC):

    def __init__(self):
        self.__data: Data
        self.indicator_values: np.ndarray[Any, np.dtype[Any]]

    def prepare_indicator(self, data: Data) -> None:
        self.__data = data
        self.indicator_values = self.calc_indicator_values(self.__data)

    def get_indicator_values(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.indicator_values

    def get_current_indicator_value(self) -> float | List[float] | Any:
        return self.indicator_values[self.__data.get_current_data_index()]

    def candlesticks_to_skip(self) -> int:
        for index, indicator in enumerate(self.indicator_values):
            if not np.isnan(indicator).any():
                return index
        return 0

    @abstractmethod
    def calc_indicator_values(self, data: Data) -> np.ndarray[Any, np.dtype[Any]]:
        pass
