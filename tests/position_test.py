import pytest

from stock_backtesting.position import Position, PositionType


def test_long_position_initialization():
    position = Position(position_type=PositionType.LONG, size=100, entry_price=50.0)

    assert position.avg_bought_price == pytest.approx(50.0, abs=0.01)
    assert position.position_type == PositionType.LONG
    assert position.size == 100


def test_short_position_initialization():
    position = Position(position_type=PositionType.SHORT, size=100, entry_price=30.0)

    assert position.avg_bought_price == pytest.approx(30.0, abs=0.01)
    assert position.position_type == PositionType.SHORT
    assert position.size == 100
