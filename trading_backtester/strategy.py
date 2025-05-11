from datetime import datetime
from typing import List, Sequence

from trading_backtester.data import CandlestickPhase, Data
from trading_backtester.indicator import Indicator
from trading_backtester.market import Market
from trading_backtester.order import Order
from trading_backtester.position import Position


class Strategy:
    def __init__(self, market: Market, positions: List[Position]):
        self.__positions = positions
        self.__candlesticks_to_skip = 0

        self._market = market

    @property
    def _positions(self) -> Sequence[Position]:
        return tuple(self.__positions)

    def collect_orders(
        self, candlestick_phase: CandlestickPhase, price: float, date_time: datetime
    ) -> List[Order]:
        raise NotImplementedError("This method should be implemented in subclasses.")

    def prepare_indicators(self, data: Data) -> None:
        for member_name in dir(self):
            member = getattr(self, member_name)
            if isinstance(member, Indicator):
                member.prepare_indicator(data)
                self.__candlesticks_to_skip = max(
                    self.__candlesticks_to_skip, member.candlesticks_to_skip()
                )

    def candletsticks_to_skip(self) -> int:
        return self.__candlesticks_to_skip
