import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

from trading_backtester.data import Data


class Plotting:

    POSITIVE_BAR_COLOR = "green"
    NEGATIVE_BAR_COLOR = "red"

    CANDLESTICK_WIDTH = 0.75

    def __init__(self, data: Data):
        self.__data = data

    def draw_plot(self):
        fig, ax = plt.subplots(
            2, 1, sharex=True, gridspec_kw={"hspace": 0.2, "height_ratios": [3, 1]}
        )
        ax_price = ax[0]
        ax_volume = ax[1]

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
