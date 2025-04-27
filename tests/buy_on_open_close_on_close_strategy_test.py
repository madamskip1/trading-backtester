import os
from datetime import datetime
from typing import List

import pytest

from stock_backtesting.backtest import Backtest
from stock_backtesting.data import Data
from stock_backtesting.market import MarketTime
from stock_backtesting.order import CloseOrder, OpenOrder, Order
from stock_backtesting.position import PositionMode, PositionType
from stock_backtesting.strategy import Strategy


class BuyOnOpenCloseOnCloseAccumulateStrategy(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Buy on open
            return [
                OpenOrder(
                    size=1,
                    position_type=PositionType.LONG,
                )
            ]

        elif market_time == MarketTime.CLOSE:
            # Close on close
            return [
                CloseOrder(
                    size=1,
                    position_to_close=self._positions[0],
                )
            ]

        return []


def test_single_day_profit_long_accumulate():
    data = Data.from_csv(
        file_path=os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )
    backtest = Backtest(data, BuyOnOpenCloseOnCloseAccumulateStrategy, money=50000)
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


class BuyOnOpenCloseOnCloseDistinctStrategy(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Buy on open
            return [
                OpenOrder(
                    size=1,
                    position_type=PositionType.LONG,
                )
            ]

        elif market_time == MarketTime.CLOSE:
            # Close on close
            return [
                CloseOrder(
                    size=1,
                    position_to_close=self._positions[0],
                )
            ]

        return []


def test_single_day_profit_long_distinct():
    data = Data.from_csv(
        file_path=os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )
    backtest = Backtest(
        data,
        BuyOnOpenCloseOnCloseDistinctStrategy,
        money=50000,
        position_mode=PositionMode.DISTINCT,
    )
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


class SellOnOpenCloseOnCloseAccumulateStrategy(Strategy):

    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Sell on open
            return [
                OpenOrder(
                    size=1,
                    position_type=PositionType.SHORT,
                )
            ]

        elif market_time == MarketTime.CLOSE:
            # Close on close
            return [
                CloseOrder(
                    size=1,
                    position_to_close=self._positions[0],
                )
            ]

        return []


def test_single_day_profit_short_accumulate():
    data = Data.from_csv(
        file_path=os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )
    backtest = Backtest(data, SellOnOpenCloseOnCloseAccumulateStrategy, money=50000)
    with pytest.raises(ValueError):
        backtest.run()


class SellOnOpenCloseOnCloseDistinctStrategy(Strategy):
    def collect_orders(
        self, market_time: MarketTime, price: float, date_time: datetime
    ) -> List[Order]:
        if market_time == MarketTime.OPEN:
            # Sell on open
            return [
                OpenOrder(
                    size=1,
                    position_type=PositionType.SHORT,
                )
            ]

        elif market_time == MarketTime.CLOSE:
            # Close on close
            return [
                CloseOrder(
                    size=1,
                    position_to_close=self._positions[0],
                )
            ]

        return []


def test_single_day_profit_short_distinct():
    data = Data.from_csv(
        file_path=os.path.join(
            os.path.dirname(__file__), "data", "^spx_01_03_2025-07_03_2025.csv"
        )
    )
    backtest = Backtest(
        data,
        SellOnOpenCloseOnCloseDistinctStrategy,
        money=50000,
        position_mode=PositionMode.DISTINCT,
    )
    stats = backtest.run()

    assert stats["total_trades"] == 10
    assert stats["total_open_trades"] == 5
    assert stats["total_close_trades"] == 5
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 5
    assert stats["total_close_short_trades"] == 5
    assert stats["final_money"] == pytest.approx(50094.33, abs=0.01)
    assert stats["final_assets_value"] == 0
    assert stats["final_total_equity"] == pytest.approx(50094.33, abs=0.01)
    assert stats["return"] == pytest.approx(94.33, abs=0.01)
    assert stats["max_drawdown"] == pytest.approx(61.27, abs=0.01)
    assert stats["max_drawdown_percentage"] == pytest.approx(0.12, abs=0.01)
