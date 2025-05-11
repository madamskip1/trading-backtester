from enum import Enum
from typing import Optional

import numpy as np


class PositionType(Enum):
    LONG = 1
    SHORT = 2


class Position:
    def __init__(
        self,
        position_type: PositionType,
        open_price: float,
        open_dateteime: np.datetime64,
        size: int,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
    ):
        self.__position_type = position_type
        self.__open_price = open_price
        self.__open_datetime = open_dateteime
        self.__size = size

        self.__validate_stop_loss(stop_loss)
        self.__validate_take_profit(take_profit)
        self.__stop_loss = stop_loss
        self.__take_profit = take_profit

    @property
    def position_type(self) -> PositionType:
        return self.__position_type

    @property
    def open_price(self) -> float:
        return self.__open_price

    @property
    def open_datetime(self) -> np.datetime64:
        return self.__open_datetime

    @property
    def size(self) -> int:
        return self.__size

    @property
    def stop_loss(self) -> Optional[float]:
        return self.__stop_loss

    @property
    def take_profit(self) -> Optional[float]:
        return self.__take_profit

    def update_stop_loss(self, stop_loss: Optional[float]) -> None:
        self.__validate_stop_loss(stop_loss)
        self.__stop_loss = stop_loss

    def update_take_profit(self, take_profit: Optional[float]) -> None:
        self.__validate_take_profit(take_profit)
        self.__take_profit = take_profit

    def calc_value(self, current_price: float) -> float:
        value = 0.0
        if self.__position_type == PositionType.LONG:
            value = current_price * self.__size
        elif self.__position_type == PositionType.SHORT:
            value = (2 * self.__open_price - current_price) * self.__size

        return value

    def replace(self, **kwargs) -> "Position":
        return Position(
            position_type=kwargs.get("position_type", self.__position_type),
            open_price=kwargs.get("open_price", self.__open_price),
            open_dateteime=kwargs.get("open_datetime", self.__open_datetime),
            size=kwargs.get("size", self.__size),
            stop_loss=kwargs.get("stop_loss", self.__stop_loss),
            take_profit=kwargs.get("take_profit", self.__take_profit),
        )

    def __validate_stop_loss(self, stop_loss: Optional[float]) -> None:
        if stop_loss is None:
            return

        if self.__position_type == PositionType.LONG:
            if stop_loss > self.__open_price:
                raise ValueError(
                    "Stop loss must be lower than open price for long position"
                )
        elif self.__position_type == PositionType.SHORT:
            if stop_loss < self.__open_price:
                raise ValueError(
                    "Stop loss must be higher than open price for short position"
                )

    def __validate_take_profit(self, take_profit: Optional[float]) -> None:
        if take_profit is None:
            return

        if self.__position_type == PositionType.LONG:
            if take_profit < self.__open_price:
                raise ValueError(
                    "Take profit must be higher than open price for long position"
                )
        elif self.__position_type == PositionType.SHORT:
            if take_profit > self.__open_price:
                raise ValueError(
                    "Take profit must be lower than open price for short position"
                )
