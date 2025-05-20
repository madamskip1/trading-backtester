from typing import Tuple, Union

import pytest

from trading_backtester.account import Account
from trading_backtester.broker import Broker, CommissionType
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
def commission_type() -> CommissionType:
    # if not provided assume relative commission
    # but it should be specified in the tests
    # where commission is used
    return CommissionType.RELATIVE


@pytest.fixture
def test_broker(
    test_data: Data,
    test_account: Account,
    spread: float,
    commission: Union[float, Tuple[float, float]],
    commission_type: CommissionType,
) -> Broker:
    return Broker(
        data=test_data,
        accout=test_account,
        spread=spread,
        commission=commission,
        commission_type=commission_type,
    )
