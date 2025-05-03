from typing import Any, List, Optional, Tuple

import pytest

from trading_backtester.data import Data


@pytest.fixture
def test_data(
    market_data: List[
        Tuple[Any, Optional[float], Optional[float], Optional[float], Optional[float]]
    ],
) -> Data:
    return Data.from_array(market_data)
