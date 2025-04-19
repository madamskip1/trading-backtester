import numpy as np
import pytest

from stock_backtesting.account import Account
from stock_backtesting.broker import Broker
from stock_backtesting.market import Market
from stock_backtesting.position import PositionMode


class MockMarket(Market):
    def __init__(self):
        super().__init__(data=np.array([]))
        self.price = 0.0

    def get_current_price(self) -> float:
        return self.price


@pytest.fixture
def mock_market() -> MockMarket:
    return MockMarket()


@pytest.fixture
def test_account() -> Account:
    return Account(data_size=1, initial_money=100)


@pytest.fixture
def test_broker_accumulate(mock_market: MockMarket, test_account: Account) -> Broker:
    return Broker(
        position_mode=PositionMode.ACCUMULATE, market=mock_market, accout=test_account
    )


@pytest.fixture
def test_broker_distinct(mock_market: MockMarket, test_account: Account) -> Broker:
    return Broker(
        position_mode=PositionMode.DISTINCT, market=mock_market, accout=test_account
    )
