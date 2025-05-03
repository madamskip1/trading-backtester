from datetime import datetime
from typing import List

from trading_backtester.data import Data
from trading_backtester.indicator import Indicator
from trading_backtester.market import Market, MarketTime
from trading_backtester.order import Order
from trading_backtester.position import Position


class Strategy:
    def __init__(self, market: Market, positions: List[Position]):
        self._market = market
        self._positions = positions
        self.__candlesticks_to_skip = 0

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        raise NotImplementedError("This method should be implemented in subclasses.")

    def prepare_indicators(self, data: Data):
        for member_name in dir(self):
            member = getattr(self, member_name)
            if isinstance(member, Indicator):
                member.prepare_indicator(data)
                self.__candlesticks_to_skip = max(
                    self.__candlesticks_to_skip, member.candlesticks_to_skip()
                )

    def candletsticks_to_skip(self) -> int:
        print(f"candlesticks_to_skip: {self.__candlesticks_to_skip}")
        return self.__candlesticks_to_skip
