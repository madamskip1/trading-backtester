import pytest

from stock_backtesting.account import Account
from stock_backtesting.broker import Broker
from stock_backtesting.data import Data
from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import CloseOrder, OpenOrder
from stock_backtesting.position import PositionType


@pytest.mark.parametrize("market_data", [[(None, 100.0, None, None, 150.0)]])
def test_close_long_accumulate_single(
    test_market: Market, test_account: Account, test_broker_accumulate: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )
    test_broker_accumulate.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_to_close=test_broker_accumulate.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders([close_order])

    assert len(test_broker_accumulate.get_trades()) == 2
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert test_broker_accumulate.get_trades()[0].market_order is True
    assert test_broker_accumulate.get_trades()[1].order == close_order
    assert test_broker_accumulate.get_trades()[1].market_order is True

    assert len(test_broker_accumulate.get_positions()) == 0
    assert test_broker_accumulate.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 50.0)]])
def test_close_long_accumulate_reduce_multiple_in_single_day(
    test_market: Market, test_account: Account, test_broker_accumulate: Broker
):
    open_order = OpenOrder(
        size=4,
        position_type=PositionType.LONG,
    )

    test_broker_accumulate.process_orders([open_order])

    close_order1 = CloseOrder(
        size=1,
        position_to_close=test_broker_accumulate.get_positions()[0],
    )
    close_order2 = CloseOrder(
        size=2,
        position_to_close=test_broker_accumulate.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders([close_order1, close_order2])

    assert len(test_broker_accumulate.get_trades()) == 3
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert test_broker_accumulate.get_trades()[0].market_order is True
    assert test_broker_accumulate.get_trades()[1].order == close_order1
    assert test_broker_accumulate.get_trades()[1].market_order is True
    assert test_broker_accumulate.get_trades()[2].order == close_order2
    assert test_broker_accumulate.get_trades()[2].market_order is True

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 1
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(50.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, 25.0, None, None, 50.0), (None, 25.0, None, None, None)]]
)
def test_close_long_accumulate_reduce_multiple_in_multiple_days(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_accumulate: Broker,
):
    open_order = OpenOrder(
        size=4,
        position_type=PositionType.LONG,
    )

    test_broker_accumulate.process_orders([open_order])

    close_order1 = CloseOrder(
        size=1,
        position_to_close=test_broker_accumulate.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders([close_order1])

    close_order2 = CloseOrder(
        size=3,
        position_to_close=test_broker_accumulate.get_positions()[0],
    )

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_accumulate.process_orders([close_order2])

    assert len(test_broker_accumulate.get_trades()) == 3
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert test_broker_accumulate.get_trades()[0].market_order is True
    assert test_broker_accumulate.get_trades()[1].order == close_order1
    assert test_broker_accumulate.get_trades()[1].market_order is True
    assert test_broker_accumulate.get_trades()[2].order == close_order2
    assert test_broker_accumulate.get_trades()[2].market_order is True

    assert len(test_broker_accumulate.get_positions()) == 0
    assert test_broker_accumulate.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(125.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, None, None, 150)]])
def test_close_long_distinct_single(
    test_market: Market, test_account: Account, test_broker_distinct: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_broker_distinct.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([close_order])

    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is True
    assert test_broker_distinct.get_trades()[1].order == close_order
    assert test_broker_distinct.get_trades()[1].market_order is True

    assert len(test_broker_distinct.get_positions()) == 0
    assert test_broker_distinct.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, 40.0, None, None, 20.0), (None, 50.0, None, None, 75.0)]]
)
def test_close_long_distinct_reduce_multiple_in_single_day(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_broker_distinct.process_orders([open_order1])

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order2])

    close_order1 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    close_order2 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[1],
    )

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders([close_order1, close_order2])

    close_order3 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([close_order3])

    assert len(test_broker_distinct.get_trades()) == 5
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[0].market_order is True
    assert test_broker_distinct.get_trades()[1].order == open_order2
    assert test_broker_distinct.get_trades()[1].market_order is True
    assert test_broker_distinct.get_trades()[2].order == close_order1
    assert test_broker_distinct.get_trades()[2].market_order is True
    assert test_broker_distinct.get_trades()[3].order == close_order2
    assert test_broker_distinct.get_trades()[3].market_order is True
    assert test_broker_distinct.get_trades()[4].order == close_order3
    assert test_broker_distinct.get_trades()[4].market_order is True

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        20.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(75.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(175.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, 40.0, None, None, 20.0), (None, 50.0, None, None, 75.0)]]
)
def test_close_long_distinct_reduce_multiple_in_multiple_days(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_broker_distinct.process_orders([open_order1])

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order2])

    close_order1 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    close_order2 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[1],
    )

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders([close_order1, close_order2])

    close_order3 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([close_order3])

    assert len(test_broker_distinct.get_trades()) == 5
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[0].market_order is True
    assert test_broker_distinct.get_trades()[1].order == open_order2
    assert test_broker_distinct.get_trades()[1].market_order is True
    assert test_broker_distinct.get_trades()[2].order == close_order1
    assert test_broker_distinct.get_trades()[2].market_order is True
    assert test_broker_distinct.get_trades()[3].order == close_order2
    assert test_broker_distinct.get_trades()[3].market_order is True
    assert test_broker_distinct.get_trades()[4].order == close_order3
    assert test_broker_distinct.get_trades()[4].market_order is True

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        20.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(75.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(175.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, None, None, 50.0)]])
def test_close_short_distinct_single(
    test_market: Market, test_account: Account, test_broker_distinct: Broker
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_broker_distinct.process_orders([open_order])

    close_order = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([close_order])

    assert len(test_broker_distinct.get_trades()) == 2
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is True
    assert test_broker_distinct.get_trades()[1].order == close_order
    assert test_broker_distinct.get_trades()[1].market_order is True

    assert len(test_broker_distinct.get_positions()) == 0
    assert test_broker_distinct.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(150.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, 20.0)]])
def test_open_short_distinct_reduce_multiple_in_single_day(
    test_market: Market, test_account: Account, test_broker_distinct: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    open_order2 = OpenOrder(
        size=3,
        position_type=PositionType.SHORT,
    )

    test_broker_distinct.process_orders([open_order1, open_order2])

    close_order1 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    close_order2 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[1],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([close_order1, close_order2])

    assert len(test_broker_distinct.get_trades()) == 4
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[0].market_order is True
    assert test_broker_distinct.get_trades()[1].order == open_order2
    assert test_broker_distinct.get_trades()[1].market_order is True
    assert test_broker_distinct.get_trades()[2].order == close_order1
    assert test_broker_distinct.get_trades()[2].market_order is True
    assert test_broker_distinct.get_trades()[3].order == close_order2
    assert test_broker_distinct.get_trades()[3].market_order is True

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker_distinct.get_positions()[0].size == 2
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(60.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(60.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, 50.0, None, None, 25.0), (None, 20.0, None, None, 15.0)]]
)
def test_open_short_distinct_multiple_in_multiple_days(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_broker_distinct.process_orders([open_order1])

    open_order2 = OpenOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order2])

    close_order1 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    close_order2 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[1],
    )

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders([close_order1, close_order2])

    close_order3 = CloseOrder(
        size=1,
        position_to_close=test_broker_distinct.get_positions()[0],
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([close_order3])

    assert len(test_broker_distinct.get_trades()) == 5
    assert test_broker_distinct.get_trades()[0].order == open_order1
    assert test_broker_distinct.get_trades()[0].market_order is True
    assert test_broker_distinct.get_trades()[1].order == open_order2
    assert test_broker_distinct.get_trades()[1].market_order is True
    assert test_broker_distinct.get_trades()[2].order == close_order1
    assert test_broker_distinct.get_trades()[2].market_order is True
    assert test_broker_distinct.get_trades()[3].order == close_order2
    assert test_broker_distinct.get_trades()[3].market_order is True
    assert test_broker_distinct.get_trades()[4].order == close_order3
    assert test_broker_distinct.get_trades()[4].market_order is True

    assert len(test_broker_distinct.get_positions()) == 0
    assert test_broker_distinct.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(145.0, abs=0.01)
