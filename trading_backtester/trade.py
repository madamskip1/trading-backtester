from enum import Enum
from typing import Optional

from trading_backtester.position import PositionType


class TradeType(Enum):
    OPEN = 1
    CLOSE = 2


class Trade:

    def __init__(
        self,
        trade_type: TradeType,
        position_type: PositionType,
        open_price: float,
        open_size: Optional[float] = None,
        close_price: Optional[float] = None,
        close_size: Optional[float] = None,
        market_order: bool = False,
    ):
        assert not (
            trade_type == TradeType.CLOSE
            and (close_price is None or close_size is None)
        ), "Close trades must have a close price and size."
        assert not (
            trade_type == TradeType.OPEN and open_size is None
        ), "Open trades must have an open size."

        self.trade_type = trade_type
        self.position_type = position_type
        self.open_price = open_price
        self.open_size = open_size
        self.close_price = close_price
        self.close_size = close_size
        self.market_order = market_order


class OpenTrade(Trade):
    def __init__(
        self, position_type: PositionType, price: float, size: float, market_order: bool
    ):
        super().__init__(
            trade_type=TradeType.OPEN,
            position_type=position_type,
            open_price=price,
            open_size=size,
            market_order=market_order,
        )


class CloseTrade(Trade):
    def __init__(
        self,
        position_type: PositionType,
        open_price: float,
        close_price: float,
        close_size: float,
        market_order: bool,
    ):
        super().__init__(
            trade_type=TradeType.CLOSE,
            position_type=position_type,
            open_price=open_price,
            close_price=close_price,
            close_size=close_size,
            market_order=market_order,
        )
