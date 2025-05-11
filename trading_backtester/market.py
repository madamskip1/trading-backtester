from typing import Optional

from trading_backtester.data import CandlestickPhase, Data


class Market:

    def __init__(self, data: Data):
        self.__data = data

    def get_current_price(self) -> float:
        return self.__data.get_current_price()

    def get_current_open_price(self) -> float:
        return self.__data.get_current_data("open")

    def get_current_close_price(self) -> float:
        if self.__data.get_candlestick_phase() != CandlestickPhase.CLOSE:
            raise ValueError(
                "Candlestick is not closed yet. Can't look into the future."
            )

        return self.__data.get_current_data("close")

    def get_current_low_price(self) -> float:
        return (
            self.__data.get_current_data("low")
            if self.__data.get_candlestick_phase() == CandlestickPhase.CLOSE
            else self.__data.get_current_data("open")
        )

    def get_current_high_price(self) -> float:
        return (
            self.__data.get_current_data("high")
            if self.__data.get_candlestick_phase() == CandlestickPhase.CLOSE
            else self.__data.get_current_data("open")
        )

    def get_open_price_on_nth_ago(self, n: int) -> Optional[float]:
        if n < 1:
            raise ValueError("To look into the past, n must be greater than 0.")

        if self.__data.get_current_data_index() - n < 0:
            return None

        return self.__data[self.__data.get_current_data_index() - n]["open"]

    def get_close_price_on_nth_ago(self, n: int) -> Optional[float]:
        if n < 1:
            raise ValueError("To look into the past, n must be greater than 0.")

        if self.__data.get_current_data_index() - n < 0:
            return None

        return self.__data[self.__data.get_current_data_index() - n]["close"]
