from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from .position import Position, PositionType


class OrderAction(Enum):
    OPEN = 1
    CLOSE = 2


class Order(ABC):
    @abstractmethod
    def __init__(
        self,
        size: int,
        action: OrderAction,
        position_type: PositionType,
        position_to_close: Optional[Position] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        limit_price: Optional[float] = None,
    ):
        self.__size = size
        self.__position_type = position_type
        self.__action = action
        self.__position_to_close = position_to_close
        self.__stop_loss = stop_loss
        self.__take_profit = take_profit
        self.__limit_price = limit_price

    @property
    def size(self) -> int:
        return self.__size

    @property
    def position_type(self) -> PositionType:
        return self.__position_type

    @property
    def action(self) -> OrderAction:
        return self.__action

    @property
    def position_to_close(self) -> Optional[Position]:
        return self.__position_to_close

    @property
    def stop_loss(self) -> Optional[float]:
        return self.__stop_loss

    @property
    def take_profit(self) -> Optional[float]:
        return self.__take_profit

    @property
    def limit_price(self) -> Optional[float]:
        return self.__limit_price


class OpenOrder(Order):
    def __init__(
        self,
        size: int,
        position_type: PositionType,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        limit_price: Optional[float] = None,
    ):
        super().__init__(
            size=size,
            action=OrderAction.OPEN,
            position_type=position_type,
            stop_loss=stop_loss,
            take_profit=take_profit,
            limit_price=limit_price,
        )


class CloseOrder(Order):
    def __init__(
        self,
        size: int,
        position_type: Optional[PositionType] = None,
        position_to_close: Optional[Position] = None,
    ):
        if position_to_close is None and position_type is None:
            raise ValueError(
                "Either position_to_close or position_type must be provided."
            )

        if position_to_close is not None:
            position_type = position_to_close.position_type

        assert position_type is not None

        super().__init__(
            size=size,
            action=OrderAction.CLOSE,
            position_type=position_type,
            position_to_close=position_to_close,
        )
