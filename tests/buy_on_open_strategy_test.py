import os
from typing import List

import pytest

from stock_backtesting.backtest import Backtest
from stock_backtesting.market import MarketTime
from stock_backtesting.order import Order, OrderAction, OrderType
from stock_backtesting.strategy import Strategy

from .utils.load_csv import load_csv


class BuyOnOpenStrategy(Strategy):

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Buy on open
            return [
                Order(
                    OrderType.MARKET_ORDER,
                    price,
                    1,
                    OrderAction.OPEN,
                )
            ]

        return []


def test_single_day_profit():
    data = load_csv(
        os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )

    backtest = Backtest(data, BuyOnOpenStrategy, money=50000)
    stats = backtest.run()

    assert stats["total_trades"] == 5
    assert stats["total_open_trades"] == 5
    assert stats["total_close_trades"] == 0
    assert stats["total_open_long_trades"] == 5
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(20926.45, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(28851.00, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(49777.45, abs=0.01)
    assert stats["return"] == pytest.approx(-222.55, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(393.46, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.79, abs=0.01)
