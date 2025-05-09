from typing import Dict, List

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

from trading_backtester.account import Account
from trading_backtester.data import Data
from trading_backtester.position import PositionType
from trading_backtester.trade import CloseTrade, Trade, TradeType


class Plotting:

    POSITIVE_BAR_COLOR = "green"
    NEGATIVE_BAR_COLOR = "red"

    CANDLESTICK_WIDTH = 0.75

    def __init__(self, data: Data, trades: List[Trade], account: Account):
        self.__data = data
        self.__trades = trades
        self.__account = account

    def draw_plot(self):
        fig, ax = plt.subplots(
            3, 1, sharex=True, gridspec_kw={"hspace": 0.2, "height_ratios": [1, 3, 1]}
        )
        ax_equity = ax[0]
        ax_price = ax[1]
        ax_volume = ax[2]

        datetime_to_index: Dict[np.datetime64, int] = {
            dt: i for i, dt in enumerate(self.__data.datetime)
        }

        for i, data in enumerate(self.__data):
            self.__draw_candlestick(
                ax_price, i, data["open"], data["high"], data["low"], data["close"]
            )
            self.__draw_volume_bar(
                ax_volume,
                i,
                data["volume"],
                self.__get_bar_color(data["open"], data["close"]),
            )

        for trade in reversed(self.__trades):
            if trade.trade_type == TradeType.CLOSE:
                assert isinstance(trade, CloseTrade)
                self.__draw_closed_trade(ax_price, trade, datetime_to_index)

        self.__draw_equity_plot(ax_equity)
        ax_price.set_ylabel("Price")
        ax_price.grid(True, axis="y")

        ax_volume.set_ylabel("Volume")
        ax_volume.grid(True, axis="y")

        ax_volume.set_xticks(list(range(len(self.__data))))

        dateformat = self.__get_date_format()
        xticklabels = [
            np.datetime64(dt)
            .astype("datetime64[s]")
            .astype(object)
            .strftime(dateformat)
            for dt in self.__data.datetime
        ]

        ax_volume.set_xticklabels(xticklabels)
        ax_volume.set_xlabel("Time")

        fig.autofmt_xdate()

        plt.show()

    def __get_bar_color(self, open_val: float, close_val: float) -> str:
        return (
            self.POSITIVE_BAR_COLOR
            if close_val >= open_val
            else self.NEGATIVE_BAR_COLOR
        )

    def __get_date_format(self) -> str:
        diffs = np.diff(self.__data.datetime)
        min_diff = np.min(diffs)

        if min_diff < np.timedelta64(1, "h"):
            return "%H:%M"
        elif min_diff < np.timedelta64(12, "h"):
            return "%m-%d %H:%M"
        elif min_diff < np.timedelta64(28, "D"):
            return "%Y-%m-%d"
        elif min_diff < np.timedelta64(365, "D"):
            return "%Y-%m"
        else:
            return "%Y"

    def __draw_candlestick(
        self,
        ax: Axes,
        i: int,
        open_val: float,
        high_val: float,
        low_val: float,
        close_val: float,
    ):
        lower = min(open_val, close_val)
        height = abs(close_val - open_val)
        bar_color = self.__get_bar_color(open_val, close_val)

        ax.plot([i, i], [low_val, high_val], color="black", zorder=2)
        ax.add_patch(
            Rectangle(
                (i - self.CANDLESTICK_WIDTH / 2, lower),
                self.CANDLESTICK_WIDTH,
                height,
                facecolor=bar_color,
                zorder=3,
            )
        )

    def __draw_volume_bar(self, ax: Axes, i: int, volume_val: float, color: str):
        ax.bar(i, volume_val, width=0.95, color=color, zorder=2)

    def __draw_closed_trade(
        self,
        ax: Axes,
        close_trade: CloseTrade,
        datetime_to_index: Dict[np.datetime64, int],
    ):
        assert close_trade.close_datetime is not None
        assert close_trade.close_price is not None

        x_start = datetime_to_index[close_trade.open_datetime]
        y_start = close_trade.open_price
        x_end = datetime_to_index[close_trade.close_datetime]
        y_end = close_trade.close_price

        marker = "^" if close_trade.position_type == PositionType.LONG else "v"
        color = self.__get_bar_color(close_trade.open_price, close_trade.close_price)

        ax.plot(
            [x_start, x_end],
            [y_start, y_end],
            color="black",
            linewidth=2,
            linestyle="--",
            zorder=4,
        )
        ax.plot(
            x_end,
            y_end,
            marker=marker,
            color=color,
            zorder=5,
            markeredgecolor="black",
            markersize=10,
        )

    def __draw_equity_plot(
        self,
        ax: Axes,
    ):
        ax.plot(self.__account.get_equity(), zorder=11, color="blue")

        percent_equity = (
            self.__account.get_equity() / self.__account.get_equity()[0] * 100
        )
        ax2 = ax.twinx()
        ax2.set_ylim(percent_equity.min(), percent_equity.max())
        formatter = FuncFormatter(lambda y, _: f"{y:.1f} %")
        ax2.yaxis.set_major_formatter(formatter)
        ax2.grid(True, axis="y")
