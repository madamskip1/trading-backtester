import pytest

from trading_backtester.stats import Statistics

from ..conftest import AccountMock


def test_final_money(account_mock: AccountMock, test_statistics: Statistics):
    account_mock.set_current_money(1000)

    assert test_statistics.get_stats()["final_money"] == 1000


def test_final_assets_value(account_mock: AccountMock, test_statistics: Statistics):
    account_mock.set_assets_value([500])

    assert test_statistics.get_stats()["final_assets_value"] == 500


def test_final_assets_value_more_days(
    account_mock: AccountMock, test_statistics: Statistics
):
    account_mock.set_assets_value([500, 400, 600])

    assert test_statistics.get_stats()["final_assets_value"] == 600


def test_final_equity(account_mock: AccountMock, test_statistics: Statistics):
    account_mock.set_equity([500.0])

    assert test_statistics.get_stats()["final_total_equity"] == 500


def test_final_equity_more_days(account_mock: AccountMock, test_statistics: Statistics):
    account_mock.set_equity([500.0, 400.0, 600.0])

    assert test_statistics.get_stats()["final_total_equity"] == 600


def test_return(account_mock: AccountMock, test_statistics: Statistics):
    account_mock.set_equity([1000, 2000])

    assert test_statistics.get_stats()["return"] == 1000


def test_drawdown(account_mock: AccountMock, test_statistics: Statistics):
    account_mock.set_equity([1000, 800, 1200])

    assert test_statistics.get_stats()["max_drawdown"] == 200
    assert test_statistics.get_stats()["max_drawdown_percentage"] == pytest.approx(
        20.0, abs=0.01
    )


def test_drawdown_after_increased_equity(
    account_mock: AccountMock, test_statistics: Statistics
):
    account_mock.set_equity([1000, 1200, 800])

    assert test_statistics.get_stats()["max_drawdown"] == 400
    assert test_statistics.get_stats()["max_drawdown_percentage"] == pytest.approx(
        33.33, abs=0.01
    )
