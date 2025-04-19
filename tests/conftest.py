import numpy as np
import pytest

from stock_backtesting.account import Account
from stock_backtesting.broker import Broker
from stock_backtesting.market import Market
from stock_backtesting.position import PositionMode


class MarketMock(Market):
    def __init__(self):
        super().__init__(data=np.array([]))
        self.price = 0.0

    def get_current_price(self) -> float:
        return self.price


@pytest.fixture
def market_mock() -> MarketMock:
    return MarketMock()


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
