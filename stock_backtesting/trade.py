from enum import Enum
from typing import Optional


class TradeType(Enum):
    LONG = 1
    SHORT = 2


class OpenTradeTime(Enum):
    OPEN = 1
    CLOSE = 2


class CloseTradeTime(Enum):
    OPEN = 1
    CLOSE = 2

class Trade:
    def __init__(self, trade_type: TradeType, size: int, entry_price: float):
        self.trade_type = trade_type
        self.size = size
        self.entry_price = entry_price
        self.exit_price: Optional[float] = None
        self.active = True

    def calc_profit(self) -> float:
        assert self.exit_price

        if self.trade_type == TradeType.LONG:
            return (self.exit_price - self.entry_price) * self.size
        else:
            return (self.entry_price - self.exit_price) * self.size

    def calc_current_value(self, current_price: float) -> float:
        if not self.active:
            return 0.0

        return current_price * self.size