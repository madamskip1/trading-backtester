from typing import Any

import numpy as np
import pytest

from trading_backtester.data import Data
from trading_backtester.indicator import Indicator


class MultipleValuesPerCandleIndicator(Indicator):

    def calc_indicator_values(self, data: Data) -> np.ndarray[Any, np.dtype[Any]]:
        return np.column_stack((data.open, data.close))


@pytest.mark.parametrize(
    "market_data",
    [
        [
            (None, 100.0, 100.0, 120.0, 110.0),
            (None, 101.0, 101.0, 121.0, 111.0),
            (None, 102.0, 102.0, 122.0, 112.0),
        ]
    ],
)
def test_multiple_values_per_candle_indicator_values(test_data: Data):
    indicator = MultipleValuesPerCandleIndicator()

    indicator.prepare_indicator(test_data)

    expected_values = np.array([[100.0, 110.0], [101.0, 111.0], [102.0, 112.0]])
    assert np.array_equal(indicator.get_indicator_values(), expected_values)
    assert np.array_equal(indicator.get_current_indicator_value(), [100.0, 110.0])


@pytest.mark.parametrize(
    "market_data",
    [
        [
            (None, 100.0, 100.0, 120.0, np.nan),
            (None, 102.0, 102.0, 122.0, 112.0),
            (None, np.nan, np.nan, np.nan, np.nan),
            (None, 102.0, 102.0, 122.0, 112.0),
        ]
    ],
)
def test_multiple_values_per_candle_indicator_with_skip(test_data: Data):
    indicator = MultipleValuesPerCandleIndicator()

    indicator.prepare_indicator(test_data)

    assert indicator.candlesticks_to_skip() == 1


@pytest.mark.parametrize(
    "market_data",
    [
        [
            (None, 100.0, 100.0, 120.0, 112.0),
            (None, 102.0, 102.0, 122.0, 112.0),
        ]
    ],
)
def test_multiple_values_per_candle_indicator_no_skip(test_data: Data):
    indicator = MultipleValuesPerCandleIndicator()

    indicator.prepare_indicator(test_data)

    assert indicator.candlesticks_to_skip() == 0


@pytest.mark.parametrize(
    "market_data",
    [
        [
            (None, 100.0, 100.0, 120.0, 110.0),
            (None, 101.0, 101.0, 121.0, 111.0),
            (None, 102.0, 102.0, 122.0, 112.0),
        ]
    ],
)
def test_multiple_values_per_candle_indicator_next_candlestick(test_data: Data):
    indicator = MultipleValuesPerCandleIndicator()

    indicator.prepare_indicator(test_data)
    test_data.increment_data_index()

    assert np.array_equal(indicator.get_current_indicator_value(), [101.0, 111.0])
