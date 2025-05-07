from typing import Any, Dict, Optional, Type

import matplotlib.pyplot as plt

from .account import Account
from .broker import Broker
from .data import Data
from .market import Market, MarketTime
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
        self.__broker = Broker(self.__market, self.__account, spread)
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

    def show_plot(self) -> None:
        fig, ax = plt.subplots(
            2, 1, sharex=True, gridspec_kw={"hspace": 0.2, "height_ratios": [3, 1]}
        )
        ax_price = ax[0]
        ax_volume = ax[1]

        bar_width = 0.75

        for i in range(len(self.__data)):
            i_data = self.__data[i]
            open_val = i_data["open"]
            high_val = i_data["high"]
            low_val = i_data["low"]
            close_val = i_data["close"]
            volume_val = i_data["volume"]

            color = "green" if close_val >= open_val else "red"
            lower = min(open_val, close_val)
            height = abs(close_val - open_val)
            print(height)

            ax_price.plot([i, i], [low_val, high_val], color="black", zorder=2)
            ax_price.add_patch(
                plt.Rectangle(
                    (i - bar_width / 2, lower),
                    bar_width,
                    height,
                    facecolor=color,
                    zorder=3,
                )
            )

            ax_volume.bar(i, volume_val, width=0.95, color=color, zorder=2)

        ax_price.set_ylabel("Price")
        ax_price.grid(True, axis="y")

        ax_volume.set_ylabel("Volume")
        ax_volume.grid(True, axis="y")

        ax_volume.set_xticks(list(range(len(self.__data))))
        ax_price.set_xticklabels([str(dt) for dt in self.__data.datetime])
        ax_price.set_xlabel("Time")

        fig.autofmt_xdate()

        plt.show()
