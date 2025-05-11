from typing import Any, Dict, Optional, Type

from trading_backtester.plotting import Plotting

from .account import Account
from .broker import Broker
from .data import CandlestickPhase, Data
from .market import Market
from .stats import Statistics
from .strategy import Strategy


class Backtester:
    def __init__(
        self,
        data: Data,
        strategy: Type[Strategy],
        money: float = 1000.0,
        spread: float = 0.0,
        benchmark: Optional[Data] = None,
    ):
        self.__data = data
        self.__market = Market(self.__data)
        self.__account = Account(data_size=len(data), initial_money=money)
        self.__broker = Broker(self.__market, self.__data, self.__account, spread)
        self.__statistics = Statistics(
            self.__broker.get_trades(), self.__account, benchmark
        )

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
            self.__data.set_candlestick_phase(CandlestickPhase.OPEN)

            self.__broker.process_stop_losses()
            self.__broker.process_take_profits()

            new_orders = self.__strategy.collect_orders(
                self.__data.get_candlestick_phase(),
                self.__data.get_current_data("open"),
                self.__data.get_current_datatime(),
            )
            self.__broker.process_orders(new_orders=new_orders)

            self.__data.set_candlestick_phase(CandlestickPhase.CLOSE)

            self.__broker.process_stop_losses()
            self.__broker.process_take_profits()

            new_orders = self.__strategy.collect_orders(
                self.__data.get_candlestick_phase(),
                self.__data.get_current_data("close"),
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

    def get_plotting(self) -> Plotting:
        return Plotting(self.__data, self.__broker.get_trades(), self.__account)
