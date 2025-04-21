from typing import List

from stock_backtesting.order import CloseOrder, OpenOrder, OrderType
from stock_backtesting.position import Position, PositionType
from stock_backtesting.stats import Statistics
from stock_backtesting.trade import Trade

from ..conftest import AccountMock


def test_open_long_position(account_mock: AccountMock):
    trades: List[Trade] = []
    statistics = Statistics(trades, account_mock)

    trades.append(
        Trade(
            order=OpenOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_type=PositionType.LONG,
            ),
            date_index=0,
            price=100,
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
        Trade(
            order=OpenOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_type=PositionType.SHORT,
            ),
            date_index=0,
            price=100,
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
        Trade(
            order=CloseOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_to_close=Position(PositionType.LONG, size=1, price=50),
            ),
            date_index=0,
            price=100,
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
        Trade(
            order=CloseOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_to_close=Position(PositionType.SHORT, size=1, price=50),
            ),
            date_index=0,
            price=100,
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
        Trade(
            order=OpenOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_type=PositionType.LONG,
            ),
            date_index=0,
            price=100,
        )
    )

    trades.append(
        Trade(
            order=CloseOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_to_close=Position(PositionType.LONG, size=1, price=50),
            ),
            date_index=1,
            price=100,
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
        Trade(
            order=OpenOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_type=PositionType.SHORT,
            ),
            date_index=0,
            price=100,
        )
    )

    trades.append(
        Trade(
            order=CloseOrder(
                order_type=OrderType.MARKET_ORDER,
                size=1,
                position_to_close=Position(PositionType.SHORT, size=1, price=50),
            ),
            date_index=1,
            price=100,
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
