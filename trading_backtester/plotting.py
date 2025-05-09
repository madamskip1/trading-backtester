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
from trading_backtester.trade import Trade, TradeType


class Plotting:

    POSITIVE_BAR_COLOR = "green"
    NEGATIVE_BAR_COLOR = "red"

    CANDLESTICK_WIDTH = 0.75

    def __init__(self, data: Data, trades: List[Trade], account: Account):
        self.__data = data
        self.__trades = trades
        self.__account = account

        self.__should_draw_candlesticks: bool
        self.__should_draw_volume: bool
        self.__should_draw_equity: bool
        self.__should_draw_trades: bool
        self.__should_draw_annotations: bool
        self.config_drawing()

    def config_drawing(
        self,
        draw_candlesticks: bool = True,
        draw_volume: bool = True,
        draw_equity: bool = True,
        draw_trades: bool = True,
        annotations: bool = True,
    ):
        self.__should_draw_candlesticks = draw_candlesticks
        self.__should_draw_volume = draw_volume
        self.__should_draw_equity = draw_equity
        self.__should_draw_trades = draw_trades
        self.__should_draw_annotations = annotations

    def draw_plot(self):
        num_of_plots = 0
        height_ratios: List[int] = []
        ax_equity_index = -1
        ax_price_index = -1
        ax_volume_index = -1

        if self.__should_draw_equity:
            ax_equity_index = num_of_plots
            num_of_plots += 1
            height_ratios.append(1)

        if self.__should_draw_candlesticks or self.__should_draw_trades:
            ax_price_index = num_of_plots
            num_of_plots += 1
            height_ratios.append(3)

        if self.__should_draw_volume:
            ax_volume_index = num_of_plots
            num_of_plots += 1
            height_ratios.append(1)

        if num_of_plots == 0:
            raise ValueError("No plots to draw. Please enable at least one plot.")
        if num_of_plots == 1:
            height_ratios = [1]

        fig, ax = plt.subplots(
            num_of_plots,
            1,
            sharex=True,
            gridspec_kw={"hspace": 0.2, "height_ratios": height_ratios},
        )

        if num_of_plots == 1:
            ax = [ax]

        if self.__should_draw_candlesticks or self.__should_draw_trades:
            self.__draw_price_plot(ax[ax_price_index])

        if self.__should_draw_volume:
            self.__draw_volume_plot(ax[ax_volume_index])

        if self.__should_draw_equity:
            self.__draw_equity_plot(ax[ax_equity_index])

        dateformat = self.__get_date_format()
        xticklabels = [
            np.datetime64(dt)
            .astype("datetime64[s]")
            .astype(object)
            .strftime(dateformat)
            for dt in self.__data.datetime
        ]
        x_axis_values = np.arange(len(self.__data))

        last_axis = ax[-1]
        last_axis.set_xticks(x_axis_values)
        last_axis.set_xticklabels(xticklabels)
        last_axis.set_xlabel("Time")

        fig.autofmt_xdate()

        plt.show()

    def __draw_price_plot(self, ax: Axes):
        ax.set_ylabel("Price")
        ax.grid(True, axis="y"),

        if self.__should_draw_candlesticks:
            self.__draw_candlesticks(ax)

        if self.__should_draw_trades:
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

        if self.__should_draw_annotations:
            equity_cursor = mplcursors.cursor(
                scatter, hover=mplcursors.HoverMode.Transient
            )

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
        closed_trades: List[Trade] = [
            trade
            for trade in reversed(self.__trades)
            if trade.trade_type == TradeType.CLOSE
        ]

        close_markers: List[Line2D] = []
        trade_lines_x_start: List[int] = []
        trade_lines_x_end: List[int] = []
        trade_lines_y_start: List[float] = []
        trade_lines_y_end: List[float] = []

        for trade in closed_trades:
            assert trade.close_datetime is not None
            assert trade.close_price is not None

            x_start = datetime_to_x_axis[trade.open_datetime]
            y_start = trade.open_price
            x_end = datetime_to_x_axis[trade.close_datetime]
            y_end = trade.close_price

            trade_lines_x_start.append(x_start)
            trade_lines_x_end.append(x_end)
            trade_lines_y_start.append(y_start)
            trade_lines_y_end.append(y_end)

            close_marker = self.__draw_closed_trade_marker(
                ax,
                x_end,
                y_end,
                trade.position_type,
                trade.open_price,
                trade.close_price,
            )
            close_markers.append(close_marker)

        ax.plot(
            [trade_lines_x_start, trade_lines_x_end],
            [trade_lines_y_start, trade_lines_y_end],
            color="black",
            linewidth=2,
            linestyle="--",
            zorder=4,
        )

        if self.__should_draw_annotations:
            close_markers_cursor = mplcursors.cursor(
                close_markers, hover=mplcursors.HoverMode.Transient
            )

            @close_markers_cursor.connect("add")
            def on_close_markers_hover(selection: Selection):
                idx = int(selection.index)
                close_trade = closed_trades[idx]
                selection.annotation.set_text(
                    f"{"Long" if close_trade.position_type == PositionType.LONG else "Short"} Trade\n"
                    f"Open: {close_trade.open_price:.2f}\n"
                    f"Close: {close_trade.close_price:.2f}\n"
                    f"Size: {close_trade.close_size:.2f}\n"
                    f"Profit/Loss: {close_trade.calc_profit_loss():.2f}"
                )
                selection.annotation.set_horizontalalignment("left")
                selection.annotation.get_bbox_patch().set_alpha(0.9)

    def __draw_closed_trade_marker(
        self,
        ax: Axes,
        x_end: int,
        y_end: float,
        position_type: PositionType,
        open_price: float,
        close_price: float,
    ) -> Line2D:
        # def __draw_closed_trade_marker(self, ax: Axes, close_trade: Trade, datetime_to_x_axis: Dict[np.datetime64, int],) -> Line2D:
        marker = "^" if position_type == PositionType.LONG else "v"
        color = self.__get_bar_color(open_price, close_price)

        close_marker = ax.plot(
            x_end,
            y_end,
            marker=marker,
            color=color,
            zorder=5,
            markeredgecolor="black",
            markersize=10,
        )[0]

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
