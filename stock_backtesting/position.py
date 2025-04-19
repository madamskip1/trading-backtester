from enum import Enum
from typing import Optional


class PositionType(Enum):
    LONG = 1
    SHORT = 2


class PositionMode(Enum):
    ACCUMULATE = 1  # Assume only long
    DISTINCT = 2


class Position:
    def __init__(
        self,
        position_type: PositionType,
        price: float = 0,
        size: int = 0,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
    ):
        self.position_type = position_type
        self.avg_bought_price = price
        self.size = size
        self.stop_loss = stop_loss
        self.take_profit = take_profit
