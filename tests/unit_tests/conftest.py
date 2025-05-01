import numpy as np
import pytest

from stock_backtesting.account import Account
from stock_backtesting.broker import Broker
from stock_backtesting.data import Data
from stock_backtesting.market import Market
from stock_backtesting.stats import Statistics


class AccountMock(Account):
    def __init__(self):
        super().__init__(data_size=1, initial_money=0.0)

    def set_current_money(self, amount: float):
        self._current_money = amount

    def set_initial_money(self, amount: float):
        self._initial_money = amount

    def set_assets_value(self, index: int, value: float):
        self._assets_value[index] = value

    def set_equity(self, index: int, value: float):
        self._equity[index] = value

    def set_data_size(self, size: int):
        assert size >= 1
        self._assets_value = np.zeros(size, dtype=float)
        self._equity = np.zeros(size, dtype=float)


@pytest.fixture
def account_mock() -> AccountMock:
    return AccountMock()


@pytest.fixture
def test_account() -> Account:
    return Account(data_size=1, initial_money=100)


@pytest.fixture
def test_market(test_data: Data) -> Market:
    return Market(test_data)


@pytest.fixture
def spread() -> float:  # if not provided assume no spread
    return 0.0


@pytest.fixture
def test_broker(test_market: Market, test_account: Account, spread: float) -> Broker:
    return Broker(market=test_market, accout=test_account, spread=spread)


@pytest.fixture
def test_statistics(account_mock: AccountMock) -> Statistics:
    return Statistics(account=account_mock, trades=[])
