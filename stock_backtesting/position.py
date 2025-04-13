from enum import Enum


class PositionType(Enum):
    LONG = 1
    SHORT = 2


class Position:
    def __init__(self, position_type: PositionType, size: int, entry_price: float):
        self.avg_bought_price = entry_price
        self.position_type = position_type
        self.size = size
