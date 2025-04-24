from typing import List

from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import Order
from stock_backtesting.position import Position


class Strategy:
    def __init__(self, market: Market, positions: List[Position]):
        self._market = market
        self._positions = positions

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        raise NotImplementedError("This method should be implemented in subclasses.")
