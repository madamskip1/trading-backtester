from enum import Enum
from typing import Optional

from .position import Position, PositionType


class OrderType(Enum):
    MARKET_ORDER = 1
    LIMIT_ORDER = 2


class OrderAction(Enum):
    OPEN = 1
    CLOSE = 2


class Order:
    def __init__(
        self,
        order_type: OrderType,
        price: float,
        size: int,
        action: OrderAction,
        position_type: Optional[PositionType] = None,  # only for open in distinct mode
        position_to_close: Optional[Position] = None,  # only for close in distinct mode
    ):
        if order_type == OrderType.LIMIT_ORDER:
            raise NotImplementedError("Limit orders are not implemented yet.")

        self.price = price
        self.size = size
        self.order_type = order_type
        self.position_type = position_type
        self.action = action
        self.position_to_close = position_to_close
