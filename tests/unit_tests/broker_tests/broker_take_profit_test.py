import pytest

from stock_backtesting.broker import Broker
from stock_backtesting.data import Data
from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import OpenOrder, OrderAction
from stock_backtesting.position import PositionType


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 101.0, None, None, None)]]
)
def test_long_equal_on_open_time(
    test_data: Data, test_market: Market, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=101.0,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 102.0, None, None, None)]]
)
def test_long_greater_on_open_time(
    test_data: Data, test_market: Market, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=101.0,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(102.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 100.5, None, None, None)]]
)
def test_long_less_on_open_time(
    test_data: Data, test_market: Market, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=101.0,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(100.5, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 100.0, 101.0)]])
def test_long_on_close_time(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=101.0,
    )

    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position


@pytest.mark.parametrize("market_data", [[(None, 100.0, 102.0, 100.0, 101.0)]])
def test_long_during_day(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=101.0,
    )

    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.9, 100.0, 100.5)]])
def test_long_less_not_happend_during_day(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=101.0,
    )

    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(100.5, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 99.0, None, None, None)]]
)
def test_short_equal_on_open_time(
    test_data: Data, test_market: Market, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=99.0,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(99.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 98.0, None, None, None)]]
)
def test_short_less_on_open_time(
    test_data: Data, test_market: Market, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=99.0,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(98.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 99.5, None, None, None)]]
)
def test_short_greater_on_open_time(
    test_data: Data, test_market: Market, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=99.0,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(100.5, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 99.0, 99.0)]])
def test_short_less_on_close_time(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=99.0,
    )

    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(99.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 98.0, 98.5)]])
def test_short_less_during_day(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=99.0,
    )

    test_broker.process_orders([open_order])
    opened_position = test_broker.get_positions()[0]

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(99.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
    assert test_broker.get_trades()[1].order.position_to_close == opened_position


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 99.1, 99.5)]])
def test_short_not_happend_during_day(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=99.0,
    )

    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(100.5, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 100.0, 101.0)]])
def test_take_profit_not_set_long(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 99.0, 99.0)]])
def test_take_profit_not_set_short(test_market: Market, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order


@pytest.mark.parametrize("market_data", [[(None, 50.0, 51.0, 50.0, 51.0)]])
def test_multiple_long_positions(test_market: Market, test_broker: Broker):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=51.0,
    )

    open_order2 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=52.0,
    )

    test_broker.process_orders([open_order1, open_order2])
    opened_position1 = test_broker.get_positions()[0]

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_assets_value() == pytest.approx(51.0, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[2].market_order is True
    assert test_broker.get_trades()[2].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[2].price == pytest.approx(51, abs=0.01)
    assert test_broker.get_trades()[2].order.size == 1
    assert test_broker.get_trades()[2].order.position_to_close == opened_position1


@pytest.mark.parametrize("market_data", [[(None, 50.0, 50.0, 49.0, 49.0)]])
def test_multiple_short_positions(test_market: Market, test_broker: Broker):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=49.0,
    )

    open_order2 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=48.0,
    )

    test_broker.process_orders([open_order1, open_order2])
    opened_position1 = test_broker.get_positions()[0]

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_assets_value() == pytest.approx(51.0, abs=0.01)
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[2].market_order is True
    assert test_broker.get_trades()[2].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[2].price == pytest.approx(49.0, abs=0.01)
    assert test_broker.get_trades()[2].order.size == 1
    assert test_broker.get_trades()[2].order.position_to_close == opened_position1


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, 95.0, 90.0, 95.0)], 2.2)]
)
def test_long_with_spread_exact_price(
    test_market: Market,
    test_broker: Broker,
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=95.0,
    )
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, 97.2, 90.0, 97.2)], 2.2)]
)
def test_long_with_spread_enough_price(
    test_market: Market,
    test_broker: Broker,
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=95.0,
    )
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(95.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, 90.0, 85.0, 85.0)], 2.2)]
)
def test_short_with_spread_exact_price(
    test_market: Market,
    test_broker: Broker,
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        take_profit=85.0,
    )
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, 90.0, 82.8, 82.8)], 2.2)]
)
def test_short_with_spread_enough_price(
    test_market: Market,
    test_broker: Broker,
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        take_profit=85.0,
    )
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_take_profits()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order.action == OrderAction.CLOSE
    assert test_broker.get_trades()[1].price == pytest.approx(85.0, abs=0.01)
    assert test_broker.get_trades()[1].order.size == 1
