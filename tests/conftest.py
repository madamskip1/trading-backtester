import numpy as np
import pytest

from stock_backtesting.account import Account
from stock_backtesting.broker import Broker
from stock_backtesting.market import Market
from stock_backtesting.position import PositionMode
from stock_backtesting.stats import Statistics


class MarketMock(Market):
    def __init__(self):
        super().__init__(data=np.array([]))
        self.price = 0.0

    def get_current_price(self) -> float:
        return self.price


@pytest.fixture
def market_mock() -> MarketMock:
    return MarketMock()


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
def test_broker_accumulate(market_mock: MarketMock, test_account: Account) -> Broker:
    return Broker(
        position_mode=PositionMode.ACCUMULATE, market=market_mock, accout=test_account
    )


@pytest.fixture
def test_broker_distinct(market_mock: MarketMock, test_account: Account) -> Broker:
    return Broker(
        position_mode=PositionMode.DISTINCT, market=market_mock, accout=test_account
    )


@pytest.fixture
def test_statistics(account_mock: AccountMock) -> Statistics:
    return Statistics(account=account_mock, trades=[])
