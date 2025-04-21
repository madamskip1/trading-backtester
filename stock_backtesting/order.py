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
        self.size = size
        self.position_type = position_type
        self.action = action
        self.position_to_close = position_to_close
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.limit_price = limit_price


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
        position_to_close: Position,
    ):
        super().__init__(
            size=size,
            action=OrderAction.CLOSE,
            position_to_close=position_to_close,
            position_type=position_to_close.position_type,
        )
