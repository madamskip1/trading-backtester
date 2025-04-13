import os
from typing import List

import pytest
from utils.load_csv import load_csv

from stock_backtesting.backtest import Backtest
from stock_backtesting.market import MarketTime
from stock_backtesting.order import Order, OrderAction, OrderType
from stock_backtesting.position import PositionType
from stock_backtesting.strategy import Strategy


class BuyOnOpenSellOnCloseStrategy(Strategy):

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Buy on open
            return [
                Order(
                    OrderType.MARKET_ORDER,
                    price,
                    1,
                    PositionType.LONG,
                    OrderAction.OPEN,
                )
            ]

        elif market_time == MarketTime.CLOSE:
            # Sell on close
            return [
                Order(
                    OrderType.MARKET_ORDER,
                    price,
                    1,
                    PositionType.LONG,
                    OrderAction.CLOSE,
                )
            ]

        return []


def test_single_day_profit():
    data = load_csv(
        os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )

    backtest = Backtest(data, BuyOnOpenSellOnCloseStrategy, money=50000)
    stats = backtest.run()

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
