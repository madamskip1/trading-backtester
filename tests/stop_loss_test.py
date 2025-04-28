from datetime import datetime
from typing import List

import pytest

from stock_backtesting.backtest import Backtest
from stock_backtesting.data import Data
from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import OpenOrder, Order
from stock_backtesting.position import Position, PositionType
from stock_backtesting.strategy import Strategy


class BuyOnOpenStrategyStopLoss(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:

        if market_time == MarketTime.CLOSE:
            return []

        self.had_trade = True
        # Buy on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.LONG,
                stop_loss=price - 1.0,
            )
        ]


def test_stop_loss_on_close_greater_long():
    data_array = [
        (None, 18.0, 18.0, 16.5, 16.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, BuyOnOpenStrategyStopLoss, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(99.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(99.0, abs=0.01)
    assert stats["return"] == pytest.approx(-1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.0, abs=0.01)


def test_stop_loss_on_close_equal_long():
    data_array = [
        (None, 18.0, 18.0, 17.0, 17.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, BuyOnOpenStrategyStopLoss, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(99.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(99.0, abs=0.01)
    assert stats["return"] == pytest.approx(-1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.0, abs=0.01)


def test_stop_loss_on_open_greater_long():
    data_array = [
        (None, 18.0, 18.0, 17.1, 17.5),
        (None, 16.5, 18.5, 16.0, 18.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, BuyOnOpenStrategyStopLoss, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 2
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(82.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(18.5, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(100.5, abs=0.01)
    assert stats["return"] == pytest.approx(0.5, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0.5, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.5, abs=0.01)


def test_stop_loss_on_open_equal_long():
    data_array = [
        (None, 18.0, 18.0, 17.5, 17.5),
        (None, 17.0, 18.0, 16.5, 18.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, BuyOnOpenStrategyStopLoss, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 2
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(82.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(18.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(100.0, abs=0.01)
    assert stats["return"] == pytest.approx(0.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0.5, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.5, abs=0.01)


class SellOnOpenStrategyStopLoss(Strategy):

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
