from typing import List, Tuple, Union

import pytest

from trading_backtester.account import Account
from trading_backtester.broker import Broker
from trading_backtester.commission import Commission, CommissionType
from trading_backtester.data import Data
from trading_backtester.spread import Spread, SpreadType
from trading_backtester.stats import Statistics
from trading_backtester.trade import Trade


@pytest.fixture
def test_account() -> Account:
    return Account(initial_money=100)


@pytest.fixture
def spread_rate() -> float:  # if not provided assume no spread
    return 0.0


@pytest.fixture
def spread_type() -> SpreadType:
    return SpreadType.FIXED


@pytest.fixture
def spread(spread_type: SpreadType, spread_rate: float) -> Spread:
    return Spread(spread_type=spread_type, spread_rate=spread_rate)


@pytest.fixture
def commission_type() -> CommissionType:
    return CommissionType.RELATIVE


@pytest.fixture
def commission_rate() -> Union[float, Tuple[float, float]]:
    return 0.0


@pytest.fixture
def commission(
    commission_type: CommissionType, commission_rate: Union[float, Tuple[float, float]]
) -> Commission:
    # if not provided assume relative commission with 0.0 rate
    # but it should be specified in the tests
    # where commission is used
    return Commission(
        commission_type=commission_type,
        commission_rate=commission_rate,
    )


@pytest.fixture
def trades_log() -> List[Trade]:
    return []


@pytest.fixture
def test_broker(
    test_data: Data,
    test_account: Account,
    spread: Spread,
    commission: Commission,
    trades_log: List[Trade],
) -> Broker:
    return Broker(
        data=test_data,
        accout=test_account,
        spread=spread,
        commission=commission,
        trades_log=trades_log,
        statistics=Statistics(trades_log, test_account, test_data),
    )
