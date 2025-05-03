import os
from datetime import datetime
from typing import List

import pytest

from stock_backtesting.backtest import Backtest
from stock_backtesting.data import Data
from stock_backtesting.market import MarketTime
from stock_backtesting.order import OpenOrder, Order
from stock_backtesting.position import PositionType
from stock_backtesting.strategy import Strategy


class ShortOnOpenStrategy(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.CLOSE:
            return []

        # Buy on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.SHORT,
            )
        ]


def test_few_days():
    data = Data.from_csv(
        file_path=os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )
    backtest = Backtest(data, ShortOnOpenStrategy, money=50000)
    stats = backtest.run()

    assert stats["total_trades"] == 5
    assert stats["total_open_trades"] == 5
    assert stats["total_close_trades"] == 0
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 5
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(20926.45, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(29296.1, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(50222.55, abs=0.01)
    assert stats["return"] == pytest.approx(222.55, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(190.23, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.38, abs=0.01)


class SellOnOpenStrategyTakeProfit(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.CLOSE:
            return []

        self.had_trade = True
        # Sell on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.SHORT,
                take_profit=price - 1.0,
            )
        ]


def test_take_profit_on_close_less_short():
    data_array = [
        (None, 18.0, 18.0, 15.0, 16.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, SellOnOpenStrategyTakeProfit, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 1
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(101.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(101.0, abs=0.01)
    assert stats["return"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.0, abs=0.01)


def test_take_profit_on_close_equal_short():
    data_array = [
        (None, 18.0, 18.0, 15.0, 17.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, SellOnOpenStrategyTakeProfit, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 1
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(101.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(101.0, abs=0.01)
    assert stats["return"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.0, abs=0.01)


def test_take_profit_on_open_less_short():
    data_array = [
        (None, 18.0, 18.0, 17.1, 17.5),
        (None, 16.5, 18.5, 16.0, 18.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, SellOnOpenStrategyTakeProfit, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 2
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(85.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(14.5, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(99.5, abs=0.01)
    assert stats["return"] == pytest.approx(-0.5, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.0, abs=0.01)


def test_take_profit_on_open_equal_short():
    data_array = [
        (None, 18.0, 18.0, 17.1, 17.5),
        (None, 17.0, 18.0, 16.1, 18.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, SellOnOpenStrategyTakeProfit, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 2
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(84.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(16.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(100.0, abs=0.01)
    assert stats["return"] == pytest.approx(0.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0.5, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.50, abs=0.01)


class SellOnOpenStrategyStopLoss(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:

        if market_time == MarketTime.CLOSE:
            return []

        # Sell on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.SHORT,
                stop_loss=price + 1.0,
            )
        ]


def test_stop_loss_on_close_less_short():
    data_array = [
        (None, 18.0, 19.5, 15.0, 19.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(
        data,
        SellOnOpenStrategyStopLoss,
        money=100.0,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 1
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(99.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(99.0, abs=0.01)
    assert stats["return"] == pytest.approx(-1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.0, abs=0.01)


def test_stop_loss_on_close_equal_short():
    data_array = [
        (None, 18.0, 19.0, 15.0, 19.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(
        data,
        SellOnOpenStrategyStopLoss,
        money=100.0,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 1
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(99.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(99.0, abs=0.01)
    assert stats["return"] == pytest.approx(-1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.0, abs=0.01)


def test_stop_loss_on_open_less_short():
    data_array = [
        (None, 18.0, 18.0, 15.0, 17.5),
        (None, 19.5, 19.5, 15.0, 18.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(
        data,
        SellOnOpenStrategyStopLoss,
        money=100.0,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 2
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(79.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(20.50, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(99.5, abs=0.01)
    assert stats["return"] == pytest.approx(-0.5, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.0, abs=0.01)


def test_stop_loss_on_open_equal_short():
    data_array = [
        (None, 18.0, 18.0, 15.0, 17.5),
        (None, 19.0, 19.0, 15.0, 18.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(
        data,
        SellOnOpenStrategyStopLoss,
        money=100.0,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 2
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(80.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(20.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(100.0, abs=0.01)
    assert stats["return"] == pytest.approx(0.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0.5, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.5, abs=0.01)
