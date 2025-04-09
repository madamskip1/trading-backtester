from enum import Enum
from typing import Any, Optional

import numpy as np


class MarketTime(Enum):
    OPEN = 1
    MID_DAY = 2
    CLOSE = 3


class Market:

    def __init__(self, data: np.ndarray[Any, np.dtype[Any]]):
        self.__data = data
        self.__current_day = -1  # not started yet
        self.__current_time = MarketTime.OPEN

    def get_current_day(self) -> int:
        return self.__current_day

    def increment_day(self):
        self.__current_day += 1

    def set_current_time(self, time: MarketTime):
        self.__current_time = time

    def get_current_price(self) -> float:
        if self.__current_time == MarketTime.OPEN:
            return self.__data[self.__current_day]["open"]

        if self.__current_time == MarketTime.MID_DAY:
            raise NotImplementedError("Mid-day price not implemented")

        return self.__data[self.__current_day]["close"]

    def get_today_open_price(self) -> float:
        return self.__data[self.__current_day]["open"]

    def get_today_close_price(self) -> float:
        if self.__current_time != MarketTime.CLOSE:
            raise ValueError("Market is not closed yet. Can't look into the future.")

        return self.__data[self.__current_day]["close"]

    def get_open_price_on_nth_day_ago(self, n: int) -> Optional[float]:
        if n < 1:
            raise ValueError("To look into the past, n must be greater than 0.")

        if self.__current_day - n < 0:
            return None

        return self.__data[self.__current_day - n]["open"]

    def get_close_price_on_nth_day_ago(self, n: int) -> Optional[float]:
        if n < 1:
            raise ValueError("To look into the past, n must be greater than 0.")

        if self.__current_day - n < 0:
            return None

        return self.__data[self.__current_day - n]["close"]
