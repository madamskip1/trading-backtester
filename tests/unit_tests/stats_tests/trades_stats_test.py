from typing import List

import numpy as np

from trading_backtester.account import Account
from trading_backtester.position import PositionType
from trading_backtester.stats import Statistics
from trading_backtester.trade import CloseTrade, OpenTrade, Trade


def test_open_long_position(test_account: Account):
    trades: List[Trade] = []
    statistics = Statistics(
        trades=trades, account=test_account, equity_log=np.array([-1])
    )

    trades.append(
        OpenTrade(
            position_type=PositionType.LONG,
            open_datetime=np.datetime64(),
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


def test_open_short_position(test_account: Account):
    trades: List[Trade] = []
    statistics = Statistics(
        trades=trades, account=test_account, equity_log=np.array([-1])
    )

    trades.append(
        OpenTrade(
            position_type=PositionType.SHORT,
            open_datetime=np.datetime64(),
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


def test_close_long_position(test_account: Account):
    trades: List[Trade] = []
    statistics = Statistics(
        trades=trades, account=test_account, equity_log=np.array([-1])
    )

    trades.append(
        CloseTrade(
            position_type=PositionType.LONG,
            open_datetime=np.datetime64(),
            open_price=50,
            close_datetime=np.datetime64(),
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


def test_close_short_position(test_account: Account):
    trades: List[Trade] = []
    statistics = Statistics(
        trades=trades, account=test_account, equity_log=np.array([-1])
    )

    trades.append(
        CloseTrade(
            position_type=PositionType.SHORT,
            open_datetime=np.datetime64(),
            open_price=50,
            close_datetime=np.datetime64(),
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


def test_open_and_close_long_position(test_account: Account):
    trades: List[Trade] = []
    statistics = Statistics(
        trades=trades, account=test_account, equity_log=np.array([-1])
    )

    trades.append(
        OpenTrade(
            position_type=PositionType.LONG,
            open_datetime=np.datetime64(),
            price=100,
            size=1,
            market_order=True,
        )
    )

    trades.append(
        CloseTrade(
            position_type=PositionType.LONG,
            open_datetime=np.datetime64(),
            open_price=50,
            close_datetime=np.datetime64(),
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


def test_open_and_close_short_position(test_account: Account):
    trades: List[Trade] = []
    statistics = Statistics(
        trades=trades, account=test_account, equity_log=np.array([-1])
    )

    trades.append(
        OpenTrade(
            position_type=PositionType.SHORT,
            open_datetime=np.datetime64(),
            price=100,
            size=1,
            market_order=True,
        )
    )

    trades.append(
        CloseTrade(
            position_type=PositionType.SHORT,
            open_datetime=np.datetime64(),
            open_price=50,
            close_datetime=np.datetime64(),
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
