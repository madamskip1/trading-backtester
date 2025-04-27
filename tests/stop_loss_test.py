from datetime import datetime
from typing import List

import pytest

from stock_backtesting.backtest import Backtest
from stock_backtesting.data import Data
from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import OpenOrder, Order
from stock_backtesting.position import Position, PositionMode, PositionType
from stock_backtesting.strategy import Strategy


class BuyOnOpenFirstDayStrategyStopLoss(Strategy):

    def __init__(self, market: Market, positions: List[Position]):
        super().__init__(market, positions)

        self.had_trade = False

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if self.had_trade:
            return []

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
    backtest = Backtest(data, BuyOnOpenFirstDayStrategyStopLoss, money=100.0)
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
    backtest = Backtest(data, BuyOnOpenFirstDayStrategyStopLoss, money=100.0)
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
        (None, 16.5, 18.5, 15.0, 18.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, BuyOnOpenFirstDayStrategyStopLoss, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(98.5, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(98.5, abs=0.01)
    assert stats["return"] == pytest.approx(-1.5, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.5, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.5, abs=0.01)


def test_stop_loss_on_open_equal_long():
    data_array = [
        (None, 18.0, 18.0, 15.0, 17.5),
        (None, 17.0, 18.0, 15.0, 18.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, BuyOnOpenFirstDayStrategyStopLoss, money=100.0)
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


class SellOnOpenFirstDayStrategyStopLoss(Strategy):

    def __init__(self, market: Market, positions: List[Position]):
        super().__init__(market, positions)

        self.had_trade = False

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if self.had_trade:
            return []

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
        SellOnOpenFirstDayStrategyStopLoss,
        money=100.0,
        position_mode=PositionMode.DISTINCT,
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
        SellOnOpenFirstDayStrategyStopLoss,
        money=100.0,
        position_mode=PositionMode.DISTINCT,
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
        SellOnOpenFirstDayStrategyStopLoss,
        money=100.0,
        position_mode=PositionMode.DISTINCT,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 1
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(98.5, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(98.5, abs=0.01)
    assert stats["return"] == pytest.approx(-1.5, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(2.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(2.0, abs=0.01)


def test_stop_loss_on_open_equal_short():
    data_array = [
        (None, 18.0, 18.0, 15.0, 17.5),
        (None, 19.0, 19.0, 15.0, 18.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(
        data,
        SellOnOpenFirstDayStrategyStopLoss,
        money=100.0,
        position_mode=PositionMode.DISTINCT,
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
    assert stats["max_drawdown"] == pytest.approx(1.5, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.5, abs=0.01)


class BuyOnOpenStrategyStopLoss(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.CLOSE:
            return []

        # Buy on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.LONG,
                stop_loss=price - 1.0,
            )
        ]


def test_rewrite_stop_loss_accumulate_mode_long():
    data_array = [
        (None, 18.0, 18.0, 17.2, 17.5),
        (None, 17.1, 17.1, 16.2, 16.9),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(data, BuyOnOpenStrategyStopLoss, money=100.0)
    stats = backtest.run()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 0
    assert stats["total_open_long_trades"] == 2
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(64.9, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(33.8, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(98.7, abs=0.01)
    assert stats["return"] == pytest.approx(-1.3, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.3, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.3, abs=0.01)


def test_stop_loss_distinct_mode_long():
    data_array = [
        (None, 18.0, 18.0, 17.1, 17.5),
        (None, 17.1, 17.1, 16.2, 16.5),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(
        data,
        BuyOnOpenStrategyStopLoss,
        money=100.0,
        position_mode=PositionMode.DISTINCT,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 2
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(81.9, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(16.5, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(98.4, abs=0.01)
    assert stats["return"] == pytest.approx(-1.6, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(1.6, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(1.6, abs=0.01)


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


def test_stop_loss_distinct_mode_short():
    data_array = [
        (None, 18.0, 18.0, 15.0, 17.5),
        (None, 18.1, 19.0, 15.0, 19.0),
    ]

    data = Data.from_array(data_array)
    backtest = Backtest(
        data,
        SellOnOpenStrategyStopLoss,
        money=100.0,
        position_mode=PositionMode.DISTINCT,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 3
    assert stats["total_open_trades"] == 2
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 2
    assert stats["total_close_short_trades"] == 1
    assert stats["final_money"] == pytest.approx(80.9, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(17.2, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(98.1, abs=0.01)
    assert stats["return"] == pytest.approx(-1.9, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(2.4, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(2.38, abs=0.01)
