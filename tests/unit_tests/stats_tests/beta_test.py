from typing import List, Optional

import numpy as np
import pytest

from trading_backtester.account import Account
from trading_backtester.data import Data
from trading_backtester.stats import Statistics


@pytest.mark.parametrize(
    "market_data, equity, expected_beta",
    [
        (
            [(None, 5.0, 5.0, 5.0, 5.0, None), (None, 5.0, 5.0, 5.0, 5.0, None)],
            [10.0, 10.0, 10.0],
            None,
        ),
        (
            [(None, 5.0, 5.0, 5.0, 5.0, None), (None, 5.0, 5.0, 5.0, 5.0, None)],
            [10.0, 15.0, 20.0],
            None,
        ),
        (
            [(None, 5.0, 10.0, 5.0, 10.0, None), (None, 10.0, 10.0, 10.0, 10.0, None)],
            [10.0, 10.0, 10.0],
            0.0,
        ),
        (
            [(None, 5.0, 10.0, 5.0, 10.0, None), (None, 10.0, 10.0, 10.0, 10.0, None)],
            [10.0, 10.0, 15.0],
            -0.5,
        ),
        (
            [(None, 5.0, 10.0, 5.0, 10.0, None), (None, 10.0, 10.0, 10.0, 10.0, None)],
            [10.0, 10.0, 5.0],
            0.5,
        ),
        (
            [(None, 5.0, 10.0, 5.0, 10.0, None), (None, 10.0, 10.0, 10.0, 10.0, None)],
            [10.0, 15.0, 15.0],
            0.5,
        ),
        (
            [(None, 5.0, 10.0, 5.0, 10.0, None), (None, 10.0, 10.0, 10.0, 10.0, None)],
            [10.0, 5.0, 5.0],
            -0.5,
        ),
        (
            [(None, 5.0, 5.0, 5.0, 5.0, None), (None, 5.0, 10.0, 5.0, 10.0, None)],
            [10.0, 10.0, 10.0],
            0.0,
        ),
        (
            [(None, 5.0, 5.0, 5.0, 5.0, None), (None, 5.0, 10.0, 5.0, 10.0, None)],
            [10.0, 10.0, 15.0],
            0.5,
        ),
        (
            [(None, 5.0, 5.0, 5.0, 5.0, None), (None, 5.0, 10.0, 5.0, 10.0, None)],
            [10.0, 10.0, 5.0],
            -0.5,
        ),
        (
            [(None, 5.0, 5.0, 5.0, 5.0, None), (None, 5.0, 10.0, 5.0, 10.0, None)],
            [10.0, 15.0, 15.0],
            -0.5,
        ),
        (
            [(None, 5.0, 5.0, 5.0, 5.0, None), (None, 5.0, 10.0, 5.0, 10.0, None)],
            [10.0, 5.0, 5.0],
            0.5,
        ),
        (
            [(None, 5.0, 10.0, 5.0, 10.0, None), (None, 10.0, 15.0, 10.0, 15.0, None)],
            [10.0, 20.0, 30.0],
            1.0,
        ),
        (
            [(None, 5.0, 10.0, 5.0, 10.0, None), (None, 10.0, 15.0, 10.0, 15.0, None)],
            [10.0, 30.0, 60.0],
            2.0,
        ),
        (
            [
                (None, 10.0, 12.0, 10.0, 12.0, None),
                (None, 12.0, 15.0, 12.0, 15.0, None),
            ],
            [10.0, 6.0, 3.0],
            -2.0,
        ),
    ],
)
def test_beta(
    test_account: Account,
    test_data: Data,
    equity: List[float],
    expected_beta: Optional[float],
):
    statistics = Statistics(
        trades=[],
        equity_log=np.array(equity),
        account=test_account,
        benchmark=test_data,
    )

    stats = statistics.get_stats()
    assert stats["beta"] == expected_beta
