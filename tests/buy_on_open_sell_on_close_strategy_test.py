import os

import numpy as np
import pytest
from utils.load_csv import load_csv

from stock_backtesting.backtest import Backtest
from stock_backtesting.market import MarketTime
from stock_backtesting.strategy import Strategy
from stock_backtesting.trade import Trade


class BuyOnOpenSellOnCloseStrategy(Strategy):

    def check_buy_signal(self, price: float, time: MarketTime) -> bool:
        return time == MarketTime.OPEN

    def check_sell_signal(self, price: float, time: MarketTime) -> bool:
        pass

    def check_close_signal(self, trade: Trade, price: float, time: MarketTime) -> bool:
        return time == MarketTime.CLOSE


def test_single_day_profit():
    data = load_csv(
        os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )

    backtest = Backtest(data, BuyOnOpenSellOnCloseStrategy, money=50000)
    stats = backtest.run()

    assert stats["total_trades"] == 5
    assert stats["total_long_trades"] == 5
    assert stats["total_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(49905.67, abs=0.01)
    assert stats["final_assets_value"] == 0
    assert stats["final_total_equity"] == pytest.approx(49905.67, abs=0.01)
    assert stats["return"] == pytest.approx(-94.33, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(152.44, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.30, abs=0.01)
