import os
from datetime import datetime
from typing import List

import pytest

from trading_backtester.backtester import Backtester
from trading_backtester.data import CandlestickPhase, Data
from trading_backtester.order import OpenOrder, Order
from trading_backtester.position import PositionType
from trading_backtester.strategy import Strategy


class LongOnOpenStrategy(Strategy):

    def collect_orders(
        self, candlestick_phase: CandlestickPhase, price: float, date_time: datetime
    ) -> List[Order]:
        if candlestick_phase == CandlestickPhase.CLOSE:
            return []

        # Buy on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.LONG,
            )
        ]


def test_few_days():
    data = Data.from_csv(
        file_path=os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )
    backtest = Backtester(data, LongOnOpenStrategy, money=50000)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
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


class LongOnOpenStrategyWithTakeProfit(Strategy):

    def collect_orders(
        self, candlestick_phase: CandlestickPhase, price: float, date_time: datetime
    ) -> List[Order]:
        if candlestick_phase == CandlestickPhase.CLOSE:
            return []

        # Buy on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.LONG,
                take_profit=price + 1.0,
            )
        ]


def test_take_profit_on_close_greater():
    data_array = [
        (None, 18.0, 19.5, 15.0, 19.5, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithTakeProfit, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(101.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(101.0, abs=0.01)
    assert stats["return"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0, abs=0.01)


def test_take_profit_on_close_equal():
    data_array = [
        (None, 18.0, 19.0, 15.0, 19.0, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithTakeProfit, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["final_money"] == pytest.approx(101.0, abs=0.01)
    assert stats["final_assets_value"] == pytest.approx(0.0, abs=0.01)
    assert stats["final_total_equity"] == pytest.approx(101.0, abs=0.01)
    assert stats["return"] == pytest.approx(1.0, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(0.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.0, abs=0.01)


def test_take_profit_on_open_greater():
    data_array = [
        (None, 18.0, 18.5, 15.0, 18.5, None),
        (None, 19.5, 19.5, 15.0, 18.5, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithTakeProfit, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
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
    assert stats["max_drawdown"] == pytest.approx(0.0, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.0, abs=0.01)


def test_take_profit_on_open_equal():
    data_array = [
        (None, 18.0, 18.5, 15.0, 18.5, None),
        (None, 19.0, 19.0, 15.0, 18.0, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithTakeProfit, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
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


class LongOnOpenStrategyWithStopLoss(Strategy):

    def collect_orders(
        self, candlestick_phase: CandlestickPhase, price: float, date_time: datetime
    ) -> List[Order]:
        if candlestick_phase == CandlestickPhase.CLOSE:
            return []

        # Buy on open
        return [
            OpenOrder(
                size=1,
                position_type=PositionType.LONG,
                stop_loss=price - 1.0,
            )
        ]


def test_stop_loss_on_close_greater():
    data_array = [
        (None, 18.0, 18.0, 16.5, 16.5, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithStopLoss, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
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


def test_stop_loss_on_close_equal():
    data_array = [
        (None, 18.0, 18.0, 17.0, 17.0, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithStopLoss, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
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


def test_stop_loss_on_open_greater():
    data_array = [
        (None, 18.0, 18.0, 17.1, 17.5, None),
        (None, 16.5, 18.5, 16.0, 18.5, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithStopLoss, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
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


def test_stop_loss_on_open_equal():
    data_array = [
        (None, 18.0, 18.0, 17.5, 17.5, None),
        (None, 17.0, 18.0, 16.5, 18.0, None),
    ]

    data = Data.from_array(data_array)
    backtest = Backtester(data, LongOnOpenStrategyWithStopLoss, money=100.0)
    backtest.run()

    stats = backtest.get_statistics().get_stats()
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
