from typing import Any, Dict, Type

import numpy as np

from .account import Account
from .broker import Broker
from .data import Data
from .market import Market, MarketTime
from .position import PositionMode
from .stats import Statistics
from .strategy import Strategy


class Backtest:
    def __init__(
        self,
        data: Data,
        strategy: Type[Strategy],
        money: float = 1000.0,
        position_mode: PositionMode = PositionMode.ACCUMULATE,
    ):
        self.__data = data
        self.__market = Market(self.__data)
        self.__account = Account(data_size=len(data), initial_money=money)
        self.__broker = Broker(position_mode, self.__market, self.__account)
        self.__statistics = Statistics(self.__broker.get_trades(), self.__account)

        self.__strategy = strategy(self.__market, self.__broker.get_positions())
        self.__strategy.prepare_indicators(self.__data)

    def run(self) -> Dict[str, Any]:
        print("Starting backtest...")
        print(f"Initial money: {self.__account.get_current_money()}")

        candlesticks_to_skip = self.__strategy.candletsticks_to_skip()
        for _ in range(candlesticks_to_skip):
            self.__account.update_assets_value(
                self.__data.get_current_data_index(), 0.0
            )
            self.__account.calculate_equity(self.__data.get_current_data_index())
            self.__data.increment_data_index()

        for _ in range(self.__strategy.candletsticks_to_skip(), len(self.__data)):
            self.__market.set_current_time(MarketTime.OPEN)

            self.__broker.process_stop_losses()
            self.__broker.process_take_profits()

            new_orders = self.__strategy.collect_orders(
                self.__market.get_current_time(),
                self.__market.get_current_open_price(),
                self.__data.get_current_datatime(),
            )
            self.__broker.process_orders(new_orders=new_orders)

            self.__market.set_current_time(MarketTime.CLOSE)

            self.__broker.process_stop_losses()
            self.__broker.process_take_profits()

            new_orders = self.__strategy.collect_orders(
                self.__market.get_current_time(),
                self.__market.get_current_close_price(),
                self.__data.get_current_datatime(),
            )
            self.__broker.process_orders(new_orders=new_orders)

            self.__account.update_assets_value(
                self.__data.get_current_data_index(), self.__broker.get_assets_value()
            )
            self.__account.calculate_equity(self.__data.get_current_data_index())

            self.__data.increment_data_index()

        print("Backtest finished.")
        print(self.__statistics)

        return self.__statistics.get_stats()
