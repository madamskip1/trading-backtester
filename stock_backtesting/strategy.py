from datetime import datetime
from typing import List

from stock_backtesting.data import Data
from stock_backtesting.indicator import Indicator
from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import Order
from stock_backtesting.position import Position


class Strategy:
    def __init__(self, market: Market, positions: List[Position]):
        self._market = market
        self._positions = positions

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        raise NotImplementedError("This method should be implemented in subclasses.")

    def prepare_indicators(self, data: Data):
        for member_name in dir(self):
            member = getattr(self, member_name)
            if isinstance(member, Indicator):
                member.prepare_indicator(data)
