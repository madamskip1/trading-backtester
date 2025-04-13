from typing import List

from stock_backtesting.order import Order

from .market import Market, MarketTime


class Strategy:
    def __init__(self, market: Market):
        self._market = market

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        raise NotImplementedError("This method should be implemented in subclasses.")
