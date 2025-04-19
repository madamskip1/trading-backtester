import pytest

from stock_backtesting.broker import Broker
from stock_backtesting.order import Order, OrderAction, OrderType
from stock_backtesting.position import PositionType

from ..conftest import MarketMock


def test_long_equal(market_mock: MarketMock, test_broker_accumulate: Broker):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
        stop_loss=99,
    )
    market_mock.price = 100
    test_broker_accumulate.process_open_orders([open_order])
    opened_position = test_broker_accumulate.get_positions()[0]

    market_mock.price = 99
    test_broker_accumulate.process_stop_losses()

    assert len(test_broker_accumulate.get_positions()) == 0
    assert len(test_broker_accumulate.get_trades()) == 2
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert (
        test_broker_accumulate.get_trades()[1].order.order_type
        == OrderType.MARKET_ORDER
    )
    assert test_broker_accumulate.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker_accumulate.get_trades()[1].price == pytest.approx(99, abs=0.01)
    assert test_broker_accumulate.get_trades()[1].order.size == 1
    assert (
        test_broker_accumulate.get_trades()[1].order.position_to_close
        == opened_position
    )

    assert test_broker_accumulate.get_assets_value() == 0


def test_long_greater(market_mock: MarketMock, test_broker_accumulate: Broker):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
        stop_loss=99,
    )

    market_mock.price = 100
    test_broker_accumulate.process_open_orders([open_order])
    opened_position = test_broker_accumulate.get_positions()[0]

    market_mock.price = 98
    test_broker_accumulate.process_stop_losses()

    assert len(test_broker_accumulate.get_positions()) == 0
    assert len(test_broker_accumulate.get_trades()) == 2
    assert test_broker_accumulate.get_assets_value() == 0
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert (
        test_broker_accumulate.get_trades()[1].order.order_type
        == OrderType.MARKET_ORDER
    )
    assert test_broker_accumulate.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker_accumulate.get_trades()[1].price == pytest.approx(98, abs=0.01)
    assert test_broker_accumulate.get_trades()[1].order.size == 1
    assert (
        test_broker_accumulate.get_trades()[1].order.position_to_close
        == opened_position
    )


def test_long_less(market_mock: MarketMock, test_broker_accumulate: Broker):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
        stop_loss=99,
    )
    market_mock.price = 100
    test_broker_accumulate.process_open_orders([open_order])

    market_mock.price = 99.5
    test_broker_accumulate.process_stop_losses()

    assert len(test_broker_accumulate.get_positions()) == 1
    assert len(test_broker_accumulate.get_trades()) == 1
    assert test_broker_accumulate.get_assets_value() == pytest.approx(99.5, abs=0.01)
    assert test_broker_accumulate.get_trades()[0].order == open_order


def test_short_equal(market_mock: MarketMock, test_broker_distinct: Broker):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
        stop_loss=101,
    )
    market_mock.price = 100
    test_broker_distinct.process_open_orders([open_order])
    opened_position = test_broker_distinct.get_positions()[0]

    market_mock.price = 101
    test_broker_distinct.process_stop_losses()

    assert len(test_broker_distinct.get_positions()) == 0
    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert (
        test_broker_distinct.get_trades()[1].order.order_type == OrderType.MARKET_ORDER
    )
    assert test_broker_distinct.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker_distinct.get_trades()[1].price == pytest.approx(101, abs=0.01)
    assert test_broker_distinct.get_trades()[1].order.size == 1
    assert (
        test_broker_distinct.get_trades()[1].order.position_to_close == opened_position
    )

    assert test_broker_distinct.get_assets_value() == 0


def test_short_less(market_mock: MarketMock, test_broker_distinct: Broker):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
        stop_loss=101,
    )
    market_mock.price = 100
    test_broker_distinct.process_open_orders([open_order])
    opened_position = test_broker_distinct.get_positions()[0]

    market_mock.price = 102
    test_broker_distinct.process_stop_losses()

    assert len(test_broker_distinct.get_positions()) == 0
    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_assets_value() == 0
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert (
        test_broker_distinct.get_trades()[1].order.order_type == OrderType.MARKET_ORDER
    )
    assert test_broker_distinct.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker_distinct.get_trades()[1].price == pytest.approx(102, abs=0.01)
    assert test_broker_distinct.get_trades()[1].order.size == 1
    assert (
        test_broker_distinct.get_trades()[1].order.position_to_close == opened_position
    )


def test_short_greater(market_mock: MarketMock, test_broker_distinct: Broker):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
        stop_loss=101,
    )
    market_mock.price = 100
    test_broker_distinct.process_open_orders([open_order])

    market_mock.price = 100.5
    test_broker_distinct.process_stop_losses()

    assert len(test_broker_distinct.get_positions()) == 1
    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_assets_value() == pytest.approx(99.5, abs=0.01)
    assert test_broker_distinct.get_trades()[0].order == open_order


def test_stop_loss_not_set_long(
    market_mock: MarketMock, test_broker_accumulate: Broker
):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )
    market_mock.price = 100
    test_broker_accumulate.process_open_orders([open_order])

    market_mock.price = 99
    test_broker_accumulate.process_stop_losses()

    assert len(test_broker_accumulate.get_positions()) == 1
    assert len(test_broker_accumulate.get_trades()) == 1
    assert test_broker_accumulate.get_assets_value() == pytest.approx(99, abs=0.01)
    assert test_broker_accumulate.get_trades()[0].order == open_order


def test_stop_loss_not_set_short(market_mock: MarketMock, test_broker_distinct: Broker):
    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
    )
    market_mock.price = 100
    test_broker_distinct.process_open_orders([open_order])

    market_mock.price = 101
    test_broker_distinct.process_stop_losses()

    assert len(test_broker_distinct.get_positions()) == 1
    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_assets_value() == pytest.approx(99, abs=0.01)
    assert test_broker_distinct.get_trades()[0].order == open_order


def test_multiple_long_positions(market_mock: MarketMock, test_broker_distinct: Broker):
    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
        stop_loss=49,
    )

    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
        stop_loss=48,
    )

    market_mock.price = 50
    test_broker_distinct.process_open_orders([open_order1, open_order2])
    opened_position1 = test_broker_distinct.get_positions()[0]

    market_mock.price = 49
    test_broker_distinct.process_stop_losses()

    assert len(test_broker_distinct.get_positions()) == 1
    assert len(test_broker_distinct.get_trades()) == 3
    assert test_broker_distinct.get_assets_value() == pytest.approx(49, abs=0.01)
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[1].order == open_order2
    assert (
        test_broker_distinct.get_trades()[2].order.order_type == OrderType.MARKET_ORDER
    )
    assert test_broker_distinct.get_trades()[2].order.action == OrderAction.CLOSE
    assert test_broker_distinct.get_trades()[2].price == pytest.approx(49, abs=0.01)
    assert test_broker_distinct.get_trades()[2].order.size == 1
    assert (
        test_broker_distinct.get_trades()[2].order.position_to_close == opened_position1
    )


def test_multiple_short_positions(
    market_mock: MarketMock, test_broker_distinct: Broker
):
    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
        stop_loss=51,
    )

    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
        stop_loss=52,
    )

    market_mock.price = 50
    test_broker_distinct.process_open_orders([open_order1, open_order2])
    opened_position1 = test_broker_distinct.get_positions()[0]

    market_mock.price = 51
    test_broker_distinct.process_stop_losses()

    assert len(test_broker_distinct.get_positions()) == 1
    assert len(test_broker_distinct.get_trades()) == 3
    assert test_broker_distinct.get_assets_value() == pytest.approx(49, abs=0.01)
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[1].order == open_order2
    assert (
        test_broker_distinct.get_trades()[2].order.order_type == OrderType.MARKET_ORDER
    )
    assert test_broker_distinct.get_trades()[2].order.action == OrderAction.CLOSE
    assert test_broker_distinct.get_trades()[2].price == pytest.approx(51, abs=0.01)
    assert test_broker_distinct.get_trades()[2].order.size == 1
    assert (
        test_broker_distinct.get_trades()[2].order.position_to_close == opened_position1
    )
