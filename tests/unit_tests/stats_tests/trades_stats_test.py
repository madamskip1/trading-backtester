from typing import List

from trading_backtester.position import PositionType
from trading_backtester.stats import Statistics
from trading_backtester.trade import CloseTrade, OpenTrade, Trade

from ..conftest import AccountMock


def test_open_long_position(account_mock: AccountMock):
    trades: List[Trade] = []
    statistics = Statistics(trades, account_mock)

    trades.append(
        OpenTrade(
            position_type=PositionType.LONG,
            price=100,
            size=1,
            market_order=True,
        )
    )

    stats = statistics.get_stats()

    assert stats["total_trades"] == 1
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 0
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0
    assert stats["max_drawdown"] == 0
    assert stats["max_drawdown_percentage"] == 0


def test_open_short_position(account_mock: AccountMock):
    trades: List[Trade] = []
    statistics = Statistics(trades, account_mock)

    trades.append(
        OpenTrade(
            position_type=PositionType.SHORT,
            price=100,
            size=1,
            market_order=True,
        )
    )

    stats = statistics.get_stats()

    assert stats["total_trades"] == 1
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 0
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 1
    assert stats["total_close_short_trades"] == 0


def test_close_long_position(account_mock: AccountMock):
    trades: List[Trade] = []
    statistics = Statistics(trades, account_mock)

    trades.append(
        CloseTrade(
            position_type=PositionType.LONG,
            open_price=50,
            close_price=100,
            close_size=1,
            market_order=True,
        )
    )

    stats = statistics.get_stats()

    assert stats["total_trades"] == 1
    assert stats["total_open_trades"] == 0
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0


def test_close_short_position(account_mock: AccountMock):
    trades: List[Trade] = []
    statistics = Statistics(trades, account_mock)

    trades.append(
        CloseTrade(
            position_type=PositionType.SHORT,
            open_price=50,
            close_price=100,
            close_size=1,
            market_order=True,
        )
    )

    stats = statistics.get_stats()

    assert stats["total_trades"] == 1
    assert stats["total_open_trades"] == 0
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 1


def test_open_and_close_long_position(account_mock: AccountMock):
    trades: List[Trade] = []
    statistics = Statistics(trades, account_mock)

    trades.append(
        OpenTrade(
            position_type=PositionType.LONG,
            price=100,
            size=1,
            market_order=True,
        )
    )

    trades.append(
        CloseTrade(
            position_type=PositionType.LONG,
            open_price=50,
            close_price=100,
            close_size=1,
            market_order=True,
        )
    )

    stats = statistics.get_stats()

    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 1
    assert stats["total_close_long_trades"] == 1
    assert stats["total_open_short_trades"] == 0
    assert stats["total_close_short_trades"] == 0


def test_open_and_close_short_position(account_mock: AccountMock):
    trades: List[Trade] = []
    statistics = Statistics(trades, account_mock)

    trades.append(
        OpenTrade(
            position_type=PositionType.SHORT,
            price=100,
            size=1,
            market_order=True,
        )
    )

    trades.append(
        CloseTrade(
            position_type=PositionType.SHORT,
            open_price=50,
            close_price=100,
            close_size=1,
            market_order=True,
        )
    )

    stats = statistics.get_stats()
    assert stats["total_trades"] == 2
    assert stats["total_open_trades"] == 1
    assert stats["total_close_trades"] == 1
    assert stats["total_open_long_trades"] == 0
    assert stats["total_close_long_trades"] == 0
    assert stats["total_open_short_trades"] == 1
    assert stats["total_close_short_trades"] == 1
