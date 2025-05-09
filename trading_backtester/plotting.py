from typing import Dict, List

import mplcursors
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter
from mplcursors import Selection

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

        x_axis_values = np.arange(len(self.__data))

        self.__draw_price_plot(ax_price)
        self.__draw_volume_plot(ax_volume)
        self.__draw_equity_plot(ax_equity)

        ax_volume.set_xticks(x_axis_values)

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

    def __draw_price_plot(self, ax: Axes):
        ax.set_ylabel("Price")
        ax.grid(True, axis="y"),

        self.__draw_candlesticks(ax)
        self.__draw_closed_trades(ax)

    def __draw_volume_plot(self, ax: Axes):
        ax.set_ylabel("Volume")
        ax.grid(True, axis="y")

        for x, data in enumerate(self.__data):
            color = self.__get_bar_color(data["open"], data["close"])
            ax.bar(
                x, data["volume"], width=0.95, color=color, edgecolor="black", zorder=2
            )

    def __draw_equity_plot(
        self,
        ax: Axes,
    ):
        ax.set_ylabel("Equity")

        ax_right = ax.twinx()
        ax_right.set_ylabel("Equity %")
        ax.grid(True, axis="y")

        equity = self.__account.get_equity()

        ax.plot(equity, zorder=11, color="blue")
        scatter = ax.scatter(np.arange(len(equity)), equity, s=10, alpha=0)

        percent_equity = equity / equity[0] * 100
        ax_right.set_ylim(
            percent_equity.min() - percent_equity.min() * 0.05,
            percent_equity.max() + percent_equity.max() * 0.05,
        )
        formatter = FuncFormatter(lambda y, _: f"{y:.1f}%")
        ax_right.yaxis.set_major_formatter(formatter)

        peaks = np.maximum.accumulate(equity)
        drawdowns = equity - peaks
        drawdowns_percentages = np.abs(drawdowns / peaks)
        drawdown_threshold = 0.02
        in_drawdown = False
        last_peak = 0
        max_drawdown = 0.0
        for i, drawdown in enumerate(drawdowns_percentages):
            if drawdown == 0.0:
                if in_drawdown:
                    if max_drawdown >= drawdown_threshold:
                        ax.axvspan(last_peak, i - 1, color="red", alpha=0.2, zorder=1)
                    in_drawdown = False
                    max_drawdown = 0.0

                last_peak = i
            else:
                in_drawdown = True
                max_drawdown = max(max_drawdown, drawdown)

        if in_drawdown and max_drawdown >= drawdown_threshold:
            ax.axvspan(
                last_peak,
                len(drawdowns_percentages) - 1,
                color="red",
                alpha=0.2,
                zorder=1,
            )

        equity_cursor = mplcursors.cursor(scatter, hover=mplcursors.HoverMode.Transient)

        @equity_cursor.connect("add")
        def on_equity_cursor_hover(selection: Selection):
            idx = int(selection.index)
            value = equity[idx]
            drawdown = drawdowns[idx]
            drawdown_percentage = drawdowns_percentages[idx] * 100
            selection.annotation.set_text(
                f"Equity: {value:.2f}\nDrawdown: {drawdown:.2f} ({abs(drawdown_percentage):.2f}%)"
            )
            selection.annotation.set_horizontalalignment("left")
            selection.annotation.get_bbox_patch().set_alpha(0.9)

    def __draw_candlesticks(self, ax: Axes):
        for x, data in enumerate(self.__data):
            candlestick_color = self.__get_bar_color(data["open"], data["close"])

            # Draw the high and low lines
            ax.plot(
                [x, x], [data["low"], data["high"]], color=candlestick_color, zorder=2
            )

            body_low = min(data["open"], data["close"])
            body_height = abs(data["close"] - data["open"])
            body_bottom_left = (x - self.CANDLESTICK_WIDTH / 2, body_low)

            # Draw the body of the candlestick
            ax.add_patch(
                Rectangle(
                    body_bottom_left,
                    self.CANDLESTICK_WIDTH,
                    body_height,
                    facecolor=candlestick_color,
                    edgecolor="black",
                    zorder=3,
                )
            )

    def __draw_closed_trades(self, ax: Axes):
        datetime_to_x_axis: Dict[np.datetime64, int] = {
            dt: x for x, dt in enumerate(self.__data.datetime)
        }
        close_markers: List[Line2D] = []
        for trade in reversed(self.__trades):
            if trade.trade_type == TradeType.CLOSE:
                assert isinstance(trade, CloseTrade)
                close_marker = self.__draw_closed_trade(ax, trade, datetime_to_x_axis)
                close_markers.append(close_marker)

        close_markers_cursor = mplcursors.cursor(
            close_markers, hover=mplcursors.HoverMode.Transient
        )

        @close_markers_cursor.connect("add")
        def on_close_markers_hover(selection: Selection):
            trade: CloseTrade = selection.artist._trade
            selection.annotation.set_text(
                f"{"Long" if trade.position_type == PositionType.LONG else "Short"} Trade\n"
                f"Open: {trade.open_price:.2f}\n"
                f"Close: {trade.close_price:.2f}\n"
                f"Size: {trade.close_size:.2f}\n"
                f"Proffit/Loss: {trade.calc_profit_loss():.2f}"
            )
            selection.annotation.set_horizontalalignment("left")
            selection.annotation.get_bbox_patch().set_alpha(0.9)

    def __draw_closed_trade(
        self,
        ax: Axes,
        close_trade: CloseTrade,
        datetime_to_x_axis: Dict[np.datetime64, int],
    ) -> Line2D:
        assert close_trade.close_datetime is not None
        assert close_trade.close_price is not None

        x_start = datetime_to_x_axis[close_trade.open_datetime]
        y_start = close_trade.open_price
        x_end = datetime_to_x_axis[close_trade.close_datetime]
        y_end = close_trade.close_price

        marker = "^" if close_trade.position_type == PositionType.LONG else "v"
        color = self.__get_bar_color(close_trade.open_price, close_trade.close_price)

        # Draw the line from the open to the close
        ax.plot(
            [x_start, x_end],
            [y_start, y_end],
            color="black",
            linewidth=2,
            linestyle="--",
            zorder=4,
        )
        # Draw the marker at the close
        close_marker = ax.plot(
            x_end,
            y_end,
            marker=marker,
            color=color,
            zorder=5,
            markeredgecolor="black",
            markersize=10,
        )[0]

        close_marker._trade = close_trade

        return close_marker

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
