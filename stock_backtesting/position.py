from enum import Enum


class PositionType(Enum):
    LONG = 1
    SHORT = 2


class PositionMode(Enum):
    ACCUMULATE = 1  # Assume only long
    DISTINCT = 2


class Position:
    def __init__(self, position_type: PositionType, price: float = 0, size: int = 0):
        self.position_type = position_type
        self.avg_bought_price = price
        self.size = size
