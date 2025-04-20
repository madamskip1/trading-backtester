from typing import List

import numpy as np
import pytest

from stock_backtesting.backtest import Backtest, BacktestingDataType
from stock_backtesting.market import MarketTime
from stock_backtesting.order import Order, OrderAction, OrderType
from stock_backtesting.position import PositionMode, PositionType
from stock_backtesting.strategy import Strategy


class BuyOnOpenFirstDayStrategyStopLoss(Strategy):

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        if market_time == MarketTime.OPEN and self._market.get_current_day() == 0:
            # Buy on open
            return [
                Order(
                    OrderType.MARKET_ORDER,
                    1,
                    OrderAction.OPEN,
                    stop_loss=price - 1.0,
                )
            ]

        return []


def test_stop_loss_on_close_greater_long():
    data = np.array(
        [
            (18.0, 16.5, 18.0, 16.5),
        ],
        dtype=BacktestingDataType,
    )

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
    data = np.array(
        [
            (18.0, 17.0, 18.0, 17.0),
        ],
        dtype=BacktestingDataType,
    )

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
    data = np.array(
        [
            (18.0, 17.1, 18.0, 17.5),
            (16.5, 15.0, 18.5, 18.5),
        ],
        dtype=BacktestingDataType,
    )

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
    data = np.array(
        [
            (18.0, 15.0, 18.0, 17.5),
            (17.0, 15.0, 18.0, 18.0),
        ],
        dtype=BacktestingDataType,
    )

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

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        if market_time == MarketTime.OPEN and self._market.get_current_day() == 0:
            # Sell on open
            return [
                Order(
                    OrderType.MARKET_ORDER,
                    1,
                    OrderAction.OPEN,
                    position_type=PositionType.SHORT,
                    stop_loss=price + 1.0,
                )
            ]

        return []


def test_stop_loss_on_close_less_short():
    data = np.array(
        [
            (18.0, 15.0, 19.5, 19.5),
        ],
        dtype=BacktestingDataType,
    )

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
    data = np.array(
        [
            (18.0, 15.0, 19.0, 19.0),
        ],
        dtype=BacktestingDataType,
    )

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
    data = np.array(
        [
            (18.0, 15.0, 18.0, 17.5),
            (19.5, 15.0, 19.5, 18.5),
        ],
        dtype=BacktestingDataType,
    )

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
    data = np.array(
        [
            (18.0, 15.0, 18.0, 17.5),
            (19.0, 15.0, 19.0, 18.0),
        ],
        dtype=BacktestingDataType,
    )

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

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Buy on open
            return [
                Order(
                    OrderType.MARKET_ORDER,
                    1,
                    OrderAction.OPEN,
                    position_type=PositionType.LONG,
                    stop_loss=price - 1.0,
                )
            ]

        return []


def test_rewrite_stop_loss_accumulate_mode_long():
    data = np.array(
        [
            (18.0, 17.2, 18.0, 17.5),
            (17.1, 16.2, 17.1, 16.9),
        ],
        dtype=BacktestingDataType,
    )

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
    data = np.array(
        [
            (18.0, 17.1, 18.0, 17.5),
            (17.1, 16.2, 17.1, 16.5),
        ],
        dtype=BacktestingDataType,
    )

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

    def collect_orders(self, market_time: MarketTime, price: float) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Sell on open
            return [
                Order(
                    OrderType.MARKET_ORDER,
                    1,
                    OrderAction.OPEN,
                    position_type=PositionType.SHORT,
                    stop_loss=price + 1.0,
                )
            ]

        return []


def test_stop_loss_distinct_mode_short():
    data = np.array(
        [
            (18.0, 15.0, 18.0, 17.5),
            (18.1, 15.0, 19.0, 19.0),
        ],
        dtype=BacktestingDataType,
    )

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
