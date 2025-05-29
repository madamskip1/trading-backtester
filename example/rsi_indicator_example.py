import os
from datetime import datetime
from typing import Any, List

import numpy as np
import talib

from trading_backtester.backtester import Backtester
from trading_backtester.commission import Commission, CommissionType
from trading_backtester.data import CandlestickPhase, Data
from trading_backtester.indicator import Indicator
from trading_backtester.order import CloseOrder, OpenOrder, Order
from trading_backtester.position import PositionType
from trading_backtester.strategy import Strategy


class RsiIndicator(Indicator):
    def __init__(self, period: int):
        super().__init__()
        self.__period = period

    def _calc_indicator_values(self, data: Data) -> np.ndarray[Any, np.dtype[Any]]:
        rsi = talib.RSI(data.close, timeperiod=self.__period)
        return rsi


class RsiStrategy(Strategy):
    def __init__(
        self,
    ):
        super().__init__()
        self.__rsi_indicator = RsiIndicator(period=14)

    def collect_orders(
        self, candlestick_phase: CandlestickPhase, price: float, date_time: datetime
    ) -> List[Order]:
        orders: List[Order] = []

        if self.__rsi_indicator[-1] < 30 and self.__rsi_indicator[0] >= 30:
            # Open a long position when RSI crosses above 30
            # and close short position if exists

            if (
                len(self._positions) != 0
                and self._positions[0].position_type == PositionType.SHORT
            ):
                # Close short position if exists
                orders.append(
                    CloseOrder(
                        size=self._positions[0].size,
                        position_type=PositionType.SHORT,
                    )
                )

            if (
                len(self._positions) == 0
                or self._positions[0].position_type != PositionType.LONG
            ):
                orders.append(
                    OpenOrder(
                        size=1,
                        position_type=PositionType.LONG,
                    )
                )

        elif self.__rsi_indicator[-1] > 70 and self.__rsi_indicator[0] <= 70:
            # Open a short position when RSI crosses below 70
            # and close long position if exists

            if (
                len(self._positions) != 0
                and self._positions[0].position_type == PositionType.LONG
            ):
                # Close long position if exists
                orders.append(
                    CloseOrder(
                        size=self._positions[0].size,
                        position_type=PositionType.LONG,
                    )
                )

            if (
                len(self._positions) == 0
                or self._positions[0].position_type != PositionType.SHORT
            ):
                orders.append(
                    OpenOrder(
                        size=1,
                        position_type=PositionType.SHORT,
                    )
                )

        return orders


if __name__ == "__main__":
    data = Data.from_csv(
        file_path="^spx_d.csv",
        delimiter=";",
    )

    commission = Commission(CommissionType.RELATIVE, 0.001)
    backtest = Backtester(
        data, RsiStrategy, money=10000, benchmark=data, commission=commission
    )
    backtest.run()

    stats = backtest.get_statistics()
    print(stats)

    plotting = backtest.get_plotting()
    plotting.show_plot()
