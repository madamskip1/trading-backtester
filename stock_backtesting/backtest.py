from typing import Any, Dict, Type

import numpy as np

from .account import Account
from .broker import Broker
from .market import Market, MarketTime
from .position import PositionMode
from .stats import Statistics
from .strategy import Strategy
from .trade import Trade

BacktestingDataType = np.dtype(
    [("open", "f8"), ("min", "f8"), ("max", "f8"), ("close", "f8")]
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
        self.__account = Account(data_size=len(data), initial_money=money)
        self.__broker = Broker(position_mode, self.__market, self.__account)
        self.__statistics = Statistics(self.__broker.get_trades(), self.__account)

        self.__strategy = strategy(self.__market, self.__broker.get_positions())

    def run(self) -> Dict[str, Any]:
        print("Starting backtest...")
        print(f"Initial money: {self.__account.get_current_money()}")

        for _ in range(self.__data_len):
            self.__market.set_current_time(MarketTime.OPEN)

            self.__broker.process_stop_losses()
            self.__broker.process_take_profits()

            new_orders = self.__strategy.collect_orders(
                self.__market.get_current_time(), self.__market.get_today_open_price()
            )
            self.__broker.process_orders(new_orders=new_orders)

            self.__market.set_current_time(MarketTime.CLOSE)

            self.__broker.process_stop_losses()
            self.__broker.process_take_profits()

            new_orders = self.__strategy.collect_orders(
                self.__market.get_current_time(), self.__market.get_today_close_price()
            )
            self.__broker.process_orders(new_orders=new_orders)

            self.__account.update_assets_value(
                self.__market.get_current_day(), self.__broker.get_assets_value()
            )
            self.__account.calculate_equity(self.__market.get_current_day())

            self.__market.next_day()

        print("Backtest finished.")
        print(self.__statistics)

        return self.__statistics.get_stats()
