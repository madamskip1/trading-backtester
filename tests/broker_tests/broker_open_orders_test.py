import pytest

from stock_backtesting.account import Account
from stock_backtesting.broker import Broker
from stock_backtesting.order import Order, OrderAction, OrderType
from stock_backtesting.position import PositionType

from ..conftest import MarketMock


def test_open_long_accumulate_single(
    market_mock: MarketMock, test_account: Account, test_broker_accumulate: Broker
):
    market_mock.price = 100.0

    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )
    test_broker_accumulate.process_open_orders([open_order])

    assert len(test_broker_accumulate.get_trades()) == 1
    assert test_broker_accumulate.get_trades()[0].order == open_order

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 1
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(100.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


def test_open_long_accumulate_multiple_in_single_day(
    market_mock: MarketMock, test_account: Account, test_broker_accumulate: Broker
):
    market_mock.price = 25.0

    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=2,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    test_broker_accumulate.process_open_orders([open_order1, open_order2])

    assert len(test_broker_accumulate.get_trades()) == 2
    assert test_broker_accumulate.get_trades()[0].order == open_order1
    assert test_broker_accumulate.get_trades()[1].order == open_order2

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 3
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(25.0, abs=0.01)


def test_open_long_accumulate_multiple_in_multiple_days(
    market_mock: MarketMock, test_account: Account, test_broker_accumulate: Broker
):
    market_mock.price = 50.0

    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    test_broker_accumulate.process_open_orders([open_order1])

    market_mock.price = 25.0
    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=2,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )
    test_broker_accumulate.process_open_orders([open_order2])

    assert len(test_broker_accumulate.get_trades()) == 2
    assert test_broker_accumulate.get_trades()[0].order == open_order1
    assert test_broker_accumulate.get_trades()[1].order == open_order2

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 3
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        33.33, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


def test_open_long_distinct_single(
    market_mock: MarketMock, test_account: Account, test_broker_distinct: Broker
):
    market_mock.price = 100.0

    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    test_broker_distinct.process_open_orders([open_order])

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(100.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


def test_open_long_distinct_multiple_in_single_day(
    market_mock: MarketMock, test_account: Account, test_broker_distinct: Broker
):
    market_mock.price = 25.0

    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=2,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    test_broker_distinct.process_open_orders([open_order1, open_order2])

    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[1].order == open_order2

    assert len(test_broker_distinct.get_positions()) == 2
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker_distinct.get_positions()[1].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[1].size == 2
    assert test_broker_distinct.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker_distinct.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(25.0, abs=0.01)


def test_open_long_distinct_multiple_in_multiple_days(
    market_mock: MarketMock, test_account: Account, test_broker_distinct: Broker
):
    market_mock.price = 50.0

    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    test_broker_distinct.process_open_orders([open_order1])

    market_mock.price = 25.0
    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=2,
        action=OrderAction.OPEN,
        position_type=PositionType.LONG,
    )

    test_broker_distinct.process_open_orders([open_order2])

    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[1].order == open_order2

    assert len(test_broker_distinct.get_positions()) == 2
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )

    assert test_broker_distinct.get_positions()[1].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[1].size == 2
    assert test_broker_distinct.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker_distinct.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


def test_open_short_accumulate(
    market_mock: MarketMock, test_account: Account, test_broker_accumulate: Broker
):
    market_mock.price = 100.0

    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
    )

    with pytest.raises(ValueError):
        test_broker_accumulate.process_open_orders([open_order])


def test_open_short_distinct_single(
    market_mock: MarketMock, test_account: Account, test_broker_distinct: Broker
):
    market_mock.price = 100.0

    open_order = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
    )

    test_broker_distinct.process_open_orders([open_order])

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(100.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


def test_open_short_distinct_multiple_in_single_day(
    market_mock: MarketMock, test_account: Account, test_broker_distinct: Broker
):
    market_mock.price = 25.0

    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
    )

    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=2,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
    )

    test_broker_distinct.process_open_orders([open_order1, open_order2])

    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[1].order == open_order2

    assert len(test_broker_distinct.get_positions()) == 2
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker_distinct.get_positions()[1].position_type == PositionType.SHORT
    assert test_broker_distinct.get_positions()[1].size == 2
    assert test_broker_distinct.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker_distinct.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(25.0, abs=0.01)


def test_open_short_distinct_multiple_in_multiple_days(
    market_mock: MarketMock, test_account: Account, test_broker_distinct: Broker
):
    market_mock.price = 50.0

    open_order1 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=1,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
    )

    test_broker_distinct.process_open_orders([open_order1])

    market_mock.price = 25.0
    open_order2 = Order(
        order_type=OrderType.MARKET_ORDER,
        size=2,
        action=OrderAction.OPEN,
        position_type=PositionType.SHORT,
    )

    test_broker_distinct.process_open_orders([open_order2])

    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[1].order == open_order2

    assert len(test_broker_distinct.get_positions()) == 2
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )

    assert test_broker_distinct.get_positions()[1].position_type == PositionType.SHORT
    assert test_broker_distinct.get_positions()[1].size == 2
    assert test_broker_distinct.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker_distinct.get_assets_value() == pytest.approx(125.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)
