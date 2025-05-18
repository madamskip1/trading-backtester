import pytest

from trading_backtester.account import Account
from trading_backtester.broker import Broker
from trading_backtester.data import Data


@pytest.fixture
def test_account() -> Account:
    return Account(initial_money=100)


@pytest.fixture
def spread() -> float:  # if not provided assume no spread
    return 0.0


@pytest.fixture
def commission() -> float:  # if not provided assume no commission
    return 0.0


@pytest.fixture
def test_broker(
    test_data: Data, test_account: Account, spread: float, commission: float
) -> Broker:
    return Broker(
        data=test_data, accout=test_account, spread=spread, commission=commission
    )
