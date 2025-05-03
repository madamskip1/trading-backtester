import pytest

from trading_backtester.account import Account
from trading_backtester.broker import Broker
from trading_backtester.data import Data
from trading_backtester.market import Market, MarketTime
from trading_backtester.order import CloseOrder, OpenOrder
from trading_backtester.position import PositionType


@pytest.mark.parametrize("market_data", [[(None, 100.0, None, None, 150.0)]])
def test_close_long_single_full(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )
    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 75.0)]])
def test_close_long_single_reduce(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=2,
        position_type=PositionType.LONG,
    )
    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(75.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(75.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, None, None, 150.0)]])
def test_close_long_single_full_position_specified(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )
    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_to_close=test_broker.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 75.0)]])
def test_close_long_single_reduce_position_specified(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=2,
        position_type=PositionType.LONG,
    )
    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_to_close=test_broker.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(75.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(75.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 50.0)]])
def test_close_long_multiple_positions_in_single_order(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(
        size=4,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(200.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 50.0)]])
def test_close_long_multiple_positions_in_single_order_reduce(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(
        size=3,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(50.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 50.0)]])
def test_close_long_multiple_positions_specified_position_close(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(
        size=3,
        position_to_close=test_broker.get_positions()[1],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(50.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 50.0)]])
def test_close_long_multiple_positions_specified_position_reduce(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(
        size=2,
        position_to_close=test_broker.get_positions()[1],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 2
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None
    assert test_broker.get_positions()[1].position_type == PositionType.LONG
    assert test_broker.get_positions()[1].size == 1
    assert test_broker.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[1].stop_loss is None
    assert test_broker.get_positions()[1].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(100.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, 25.0, None, None, 50.0), (None, 25.0, None, None, None)]]
)
def test_close_long_reduce_in_multiple_candlesticks(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(
        size=4,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order])

    close_order1 = CloseOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order1])

    close_order2 = CloseOrder(
        size=3,
        position_to_close=test_broker.get_positions()[0],
    )

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders([close_order2])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order1
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order2
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(125.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 25.0)]])
def test_close_short_single_full(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 25.0)]])
def test_close_short_single_reduce(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(75.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(75.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 25.0)]])
def test_close_short_single_full_specified_position(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=2,
        position_to_close=test_broker.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 25.0)]])
def test_close_short_single_reduce_specified_position(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_to_close=test_broker.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(75.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(75.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 20.0)]])
def test_open_short_multiple_positions_in_single_order(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(
        size=4,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(120.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 20.0)]])
def test_open_short_multiple_positions_in_single_order_reduce(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(
        size=3,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(30.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(90.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 20.0)]])
def test_open_short_multiple_positions_specified_position_close(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(size=3, position_to_close=test_broker.get_positions()[1])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(30.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(90.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 20.0)]])
def test_open_short_multiple_positions_specified_position_reduec(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order1, open_order2])

    close_order = CloseOrder(size=2, position_to_close=test_broker.get_positions()[1])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order1
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == open_order2
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 2
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_positions()[1].position_type == PositionType.SHORT
    assert test_broker.get_positions()[1].size == 1
    assert test_broker.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[1].stop_loss is None
    assert test_broker.get_positions()[1].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(60.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(60.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, 25.0, None, None, 20.0), (None, 15.0, None, None, 15.0)]]
)
def test_open_short_reduce_in_multiple_candlesticks(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(
        size=4,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order])

    close_order1 = CloseOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order1])

    close_order2 = CloseOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders([close_order2])

    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order1
    assert test_broker.get_trades()[1].market_order is True
    assert test_broker.get_trades()[2].order == close_order2
    assert test_broker.get_trades()[2].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(130.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, None, None, 95.0)], 2.2)]
)
def test_close_long_with_spread(
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
    # spread: float
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )
    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.6, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, None, None, 85.0)], 2.2)]
)
def test_close_short_with_spread(
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
    # spread: float
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )
    test_broker.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([close_order])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].order == open_order
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].order == close_order
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.6, abs=0.01)
