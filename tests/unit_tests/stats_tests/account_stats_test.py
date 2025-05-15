import numpy as np
import pytest

from trading_backtester.account import Account
from trading_backtester.stats import Statistics


def test_final_assets_value_more_days(test_account: Account):
    equity_log = np.array([1000, 2000, 1500])
    statistics = Statistics(trades=[], account=test_account, equity_log=equity_log)

    assert statistics.get_stats()["final_assets_value"] == (
        1500.0 - test_account.current_money
    )


def test_return(test_account: Account):
    equity_log = np.array([1000, 2000])
    statistics = Statistics(trades=[], account=test_account, equity_log=equity_log)

    assert statistics.get_stats()["return"] == 1000
    assert statistics.get_stats()["return_percentage"] == pytest.approx(100.0, abs=0.01)


def test_drawdown(test_account: Account):
    equity_log = np.array([1000, 800, 1200])
    statistics = Statistics(trades=[], account=test_account, equity_log=equity_log)

    assert statistics.get_stats()["max_drawdown"] == 200
    assert statistics.get_stats()["max_drawdown_percentage"] == pytest.approx(
        20.0, abs=0.01
    )


def test_drawdown_after_increased_equity(test_account: Account):
    equity_log = np.array([1000, 1200, 800])
    statistics = Statistics(trades=[], account=test_account, equity_log=equity_log)

    assert statistics.get_stats()["max_drawdown"] == 400
    assert statistics.get_stats()["max_drawdown_percentage"] == pytest.approx(
        33.33, abs=0.01
    )
