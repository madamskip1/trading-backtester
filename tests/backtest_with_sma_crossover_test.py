from datetime import datetime
from typing import Any, List

import numpy as np
import pytest

from stock_backtesting.backtest import Backtest
from stock_backtesting.data import Data
from stock_backtesting.indicator import Indicator
from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import CloseOrder, OpenOrder, Order
from stock_backtesting.position import Position, PositionMode, PositionType
from stock_backtesting.strategy import Strategy


class SMAIndicator(Indicator):
    def __init__(self, period: int):
        super().__init__()
        self.period = period

    def calc_indicator_values(self, data: Data) -> np.ndarray[Any, np.dtype[Any]]:
        sma = np.convolve(data.close, np.ones(self.period) / self.period, mode="valid")
        return np.concatenate([np.full(self.period - 1, np.nan), sma])


class SMACrossoverStrategy(Strategy):
    def __init__(self, market: Market, positions: List[Position]):
        super().__init__(market, positions)
        self.short_sma = SMAIndicator(period=2)
        self.long_sma = SMAIndicator(period=3)

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.OPEN:
            return []

        orders: List[Order] = []

        current_short_sma = self.short_sma[0]
        current_long_sma = self.long_sma[0]
        previous_short_sma = self.short_sma[-1]
        previous_long_sma = self.long_sma[-1]

        assert isinstance(current_short_sma, float)
        assert isinstance(current_long_sma, float)
        assert isinstance(previous_short_sma, float)
        assert isinstance(previous_long_sma, float)

        if (
            current_short_sma > current_long_sma
            and previous_short_sma <= previous_long_sma
        ):
            orders.append(OpenOrder(size=1, position_type=PositionType.LONG))
        elif (
            current_short_sma < current_long_sma
            and previous_short_sma >= previous_long_sma
        ):
            orders.append(CloseOrder(size=1, position_to_close=self._positions[0]))

        return orders


@pytest.mark.parametrize(
    "market_data",
    [
        [
            (None, 3.0, 3.0, 3.0, 3.0),
            (None, 2.0, 2.0, 2.0, 2.0),  # SMA(2) == 2.5, SMA(3) = NaN
            (None, 1.0, 1.0, 1.0, 1.0),  # SMA(2) == 1.5, SMA(3) = 2.0
            (
                None,
                4.0,
                4.0,
                4.0,
                4.0,
            ),  # SMA(2) == 2.5, SMA(3) = 2.33 -> will cross and open long
            (None, 1.0, 1.0, 1.0, 1.0),  # SMA(2) == 2.5, SMA(3) = 2.0 -
            (
                None,
                1.0,
                1.0,
                1.0,
                1.0,
            ),  # SMA(2) == 1.0, SMA(3) = 2.0 -> will cross and close long
        ]
    ],
)
def test_sma_crossover_strategy(test_data: Data):
    backtest = Backtest(
        data=test_data,
        strategy=SMACrossoverStrategy,
        money=10.0,
        position_mode=PositionMode.ACCUMULATE,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(7.0, abs=0.01)
    assert stats["final_assets_value"] == 0
    assert stats["final_total_equity"] == pytest.approx(7.0, abs=0.01)
    assert stats["return"] == pytest.approx(-3.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(3.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(30.0, abs=0.01)
