from typing import Optional, Type

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
        self.__account = Account(data_size=len(data), initial_money=money)
        self.__broker = Broker(self.__data, self.__account, spread)
        self.__statistics = Statistics(
            self.__broker.get_trades(), self.__account, benchmark
        )

        self.__strategy = strategy(Market(self.__data), self.__broker.get_positions())
        self.__strategy.prepare_indicators(self.__data)

    def run(self) -> None:
        for _ in range(self.__strategy.candletsticks_to_skip()):
            self.__account.update_assets_value(
                self.__data.get_current_data_index(), 0.0
            )
            self.__account.calculate_equity(self.__data.get_current_data_index())
            self.__data.increment_data_index()

        for _ in range(self.__strategy.candletsticks_to_skip(), len(self.__data)):
            self.__process_candlestick_phase(CandlestickPhase.OPEN)
            self.__process_candlestick_phase(CandlestickPhase.CLOSE)

            self.__account.update_assets_value(
                self.__data.get_current_data_index(), self.__broker.get_assets_value()
            )
            self.__account.calculate_equity(self.__data.get_current_data_index())

            self.__data.increment_data_index()

    def get_statistics(self) -> Statistics:
        return self.__statistics

    def get_plotting(self) -> Plotting:
        return Plotting(self.__data, self.__broker.get_trades(), self.__account)

    def __process_candlestick_phase(self, phase: CandlestickPhase) -> None:
        self.__data.set_candlestick_phase(phase)

        self.__broker.process_stop_losses()
        self.__broker.process_take_profits()

        new_orders = self.__strategy.collect_orders(
            phase,
            self.__data.get_current_price(),
            self.__data.get_current_datatime(),
        )
        self.__broker.process_new_orders(new_orders=new_orders)
        self.__broker.process_limit_orders()
