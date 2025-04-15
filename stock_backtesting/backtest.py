from typing import Any, Dict, Type

import numpy as np

from stock_backtesting.broker import Broker

from .account import Account
from .market import Market, MarketTime
from .position import PositionMode
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
        position_mode: PositionMode = PositionMode.ACCUMULATE,
    ):
        self.__data_len = len(data)
        self.__market = Market(data)
        self.__strategy = strategy(self.__market)
        self.__account = Account(data_size=len(data), initial_money=money)
        self.__broker = Broker(position_mode, self.__market, self.__account)

        self.__statistics = Statistics(self.__broker.get_trades(), self.__account)

    def run(self) -> Dict[str, Any]:
        print("Starting backtest...")
        print(f"Initial money: {self.__account.get_current_money()}")

        for _ in range(self.__data_len):
            self.__market.increment_day()
            self.__market.set_current_time(MarketTime.OPEN)

            orders = self.__strategy.collect_orders(
                self.__market.get_current_time(), self.__market.get_today_open_price()
            )

            self.__broker.process_close_orders(orders)
            self.__broker.process_open_orders(orders)

            self.__market.set_current_time(MarketTime.MID_DAY)

            self.__market.set_current_time(MarketTime.CLOSE)

            orders = self.__strategy.collect_orders(
                self.__market.get_current_time(), self.__market.get_today_close_price()
            )

            self.__broker.process_close_orders(orders)
            self.__broker.process_open_orders(orders)

            self.__account.update_assets_value(
                self.__market.get_current_day(), self.__broker.get_assets_value()
            )
            self.__account.calculate_equity(self.__market.get_current_day())

        print("Backtest finished.")
        print(self.__statistics)

        return self.__statistics.get_stats()
