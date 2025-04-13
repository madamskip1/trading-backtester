from typing import Any, Dict, List, Type

import numpy as np

from stock_backtesting.order import Order, OrderAction

from .account import Account
from .market import Market, MarketTime
from .position import Position, PositionType
from .stats import Statistics
from .strategy import Strategy
from .trade import Trade

BacktestingDataType = np.dtype(
    [("min", "f8"), ("max", "f8"), ("open", "f8"), ("close", "f8")]
)


class Backtest:
    def __init__(
        self,
        data: np.ndarray[Any, np.dtype[Any]],
        strategy: Type[Strategy],
        money: float = 1000.0,
    ):
        self.__market = Market(data)
        self.__strategy = strategy(self.__market)
        self.__data_len = len(data)

        self.trades: List[Trade] = []
        self.long_position = Position(PositionType.LONG, 0, 0.0)
        self.short_position = Position(PositionType.SHORT, 0, 0.0)

        self.__account = Account(data_size=len(data), initial_money=money)
        self.__statistics = Statistics(self.trades, self.__account)

    def run(self) -> Dict[str, Any]:
        print("Starting backtest...")
        print(f"Initial money: {self.__account.get_current_money()}")

        for _ in range(self.__data_len):
            self.__market.increment_day()
            self.__market.set_current_time(MarketTime.OPEN)

            orders = self.__strategy.collect_orders(
                self.__market.get_current_time(), self.__market.get_today_open_price()
            )

            self.process_close_orders(orders)
            self.process_open_orders(orders)

            self.__market.set_current_time(MarketTime.MID_DAY)

            self.__market.set_current_time(MarketTime.CLOSE)

            orders = self.__strategy.collect_orders(
                self.__market.get_current_time(), self.__market.get_today_close_price()
            )

            self.process_close_orders(orders)
            self.process_open_orders(orders)

            assets_value = 0.0
            assets_value += (
                self.long_position.size * self.__market.get_today_close_price()
            )
            assets_value += (
                self.short_position.size * self.__market.get_today_close_price()
            )

            self.__account.update_assets_value(
                self.__market.get_current_day(), assets_value
            )
            self.__account.calculate_equity(self.__market.get_current_day())

        print("Backtest finished.")
        print(self.__statistics)

        return self.__statistics.get_stats()

    def process_close_orders(self, orders: List[Order]) -> None:
        for order in orders:
            if order.action == OrderAction.CLOSE:
                money = order.size * self.__market.get_current_price()
                self.__account.update_money(money)
                if order.position_type == PositionType.LONG:
                    self.long_position.size -= order.size
                elif order.position_type == PositionType.SHORT:
                    self.short_position.size -= order.size

                self.trades.append(Trade(order, self.__market.get_current_day()))

    def process_open_orders(self, orders: List[Order]) -> None:
        for order in orders:
            if order.action == OrderAction.OPEN:
                money = order.size * self.__market.get_current_price()
                self.__account.update_money(-money)
                if order.position_type == PositionType.LONG:
                    self.long_position.size += order.size
                elif order.position_type == PositionType.SHORT:
                    self.short_position.size += order.size

                self.trades.append(Trade(order, self.__market.get_current_day()))
