from datetime import datetime
from typing import List, Sequence

from trading_backtester.account import Account
from trading_backtester.data import CandlestickPhase, Data
from trading_backtester.indicator import Indicator
from trading_backtester.market import Market
from trading_backtester.order import Order
from trading_backtester.position import Position


class Strategy:
    def __init__(self):
        self.__positions: List[Position]
        self.__candlesticks_to_skip = 0
        self.__account: Account
        self.__market: Market

    @property
    def _market(self) -> Market:
        return self.__market

    @property
    def _positions(self) -> Sequence[Position]:
        assert self.__positions is not None, "Positions have not been set."
        return tuple(self.__positions)

    @property
    def _current_money(self) -> float:
        assert self.__account is not None, "Account has not been set."
        return self.__account.get_current_money()

    @property
    def _current_equity(self) -> float:
        assert self.__account is not None, "Account has not been set."
        return self.__account.get_current_equity()

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

    def set_positions(self, positions: List[Position]) -> None:
        self.__positions = positions

    def set_account(self, account: Account) -> None:
        self.__account = account

    def set_market(self, market: Market) -> None:
        self.__market = market
