import os
from datetime import datetime
from typing import List

import pytest

from trading_backtester.backtester import Backtester
from trading_backtester.data import CandlestickPhase, Data
from trading_backtester.order import CloseOrder, OpenOrder, Order
from trading_backtester.position import PositionType
from trading_backtester.strategy import Strategy


class BuyOnOpenCloseOnCloseStrategy(Strategy):

    def collect_orders(
        self, candlestick_phase: CandlestickPhase, price: float, date_time: datetime
    ) -> List[Order]:
        if candlestick_phase == CandlestickPhase.OPEN:
            # Buy on open
            return [
                OpenOrder(
                    size=1,
                    position_type=PositionType.LONG,
                )
            ]

        elif candlestick_phase == CandlestickPhase.CLOSE:
            # Close on close
            return [
                CloseOrder(
                    size=1,
                    position_to_close=self._positions[0],
                )
            ]

        return []


def test_single_day_profit_long():
    data = Data.from_csv(
        file_path=os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )
    backtest = Backtester(data, BuyOnOpenCloseOnCloseStrategy, money=50000)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
    assert stats["total_trades"] == 10
    assert stats["total_open_trades"] == 5
    assert stats["total_close_trades"] == 5
    assert stats["total_open_long_trades"] == 5
    assert stats["total_close_long_trades"] == 5
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(49905.67, abs=0.01)
    assert stats["final_assets_value"] == 0
    assert stats["final_total_equity"] == pytest.approx(49905.67, abs=0.01)
    assert stats["return"] == pytest.approx(-94.33, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(152.44, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.30, abs=0.01)
