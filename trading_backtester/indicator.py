from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np

from trading_backtester.data import Data


class Indicator(ABC):

    def __init__(self):
        self.__data: Data
        self.__indicator_values: np.ndarray[Any, np.dtype[Any]]

    def __getitem__(self, index: int) -> float | List[float] | Any:
        if index > 0:
            raise IndexError(
                "Index must be 0 or negative (if you want to access past values)"
            )

        if index < 0:
            return self.__indicator_values[self.__data.get_current_data_index() + index]

        return self.get_current_indicator_value()

    def prepare_indicator(self, data: Data) -> None:
        self.__data = data
        self.__indicator_values = self.calc_indicator_values(self.__data)

    def get_indicator_values(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__indicator_values

    def get_current_indicator_value(self) -> float | List[float] | Any:
        return self.__indicator_values[self.__data.get_current_data_index()]

    def candlesticks_to_skip(self) -> int:
        for index, indicator in enumerate(self.__indicator_values):
            if not np.isnan(indicator).any():
                return index
        return 0

    @abstractmethod
    def calc_indicator_values(self, data: Data) -> np.ndarray[Any, np.dtype[Any]]:
        pass
