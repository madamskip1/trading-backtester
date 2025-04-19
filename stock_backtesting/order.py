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
        size: int,
        action: OrderAction,
        position_type: Optional[PositionType] = None,  # only for open in distinct mode
        position_to_close: Optional[Position] = None,  # only for close in distinct mode
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        # limit_price: Optional[float] = None,  # only for limit orders TODO
    ):
        if order_type == OrderType.LIMIT_ORDER:
            raise NotImplementedError("Limit orders are not implemented yet.")

        self.size = size
        self.order_type = order_type
        self.position_type = position_type
        self.action = action
        self.position_to_close = position_to_close
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        # self.limit_price = limit_price
