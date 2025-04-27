import pytest

from stock_backtesting.account import Account
from stock_backtesting.broker import Broker
from stock_backtesting.data import Data
from stock_backtesting.market import Market, MarketTime
from stock_backtesting.order import OpenOrder
from stock_backtesting.position import PositionType


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 90.0, 90.0)]])
def test_open_long_accumulate_on_close(
    test_market: Market, test_account: Account, test_broker_accumulate: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker_accumulate.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders()

    assert len(test_broker_accumulate.get_trades()) == 1
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert test_broker_accumulate.get_trades()[0].market_order is False

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 1
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 85.0, 90.0)]])
def test_open_long_accumulate_during_day(
    test_market: Market, test_account: Account, test_broker_accumulate: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker_accumulate.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders()

    assert len(test_broker_accumulate.get_trades()) == 1
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert test_broker_accumulate.get_trades()[0].market_order is False

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 1
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 95.0), (None, 90.0, None, None, None)]]
)
def test_open_long_accumulate_on_open_equal(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_accumulate: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_accumulate.process_orders()

    assert len(test_broker_accumulate.get_trades()) == 1
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert test_broker_accumulate.get_trades()[0].market_order is False

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 1
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 95.0), (None, 85.0, None, None, None)]]
)
def test_open_long_accumulate_on_open_less(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_accumulate: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_accumulate.process_orders()

    assert len(test_broker_accumulate.get_trades()) == 1
    assert test_broker_accumulate.get_trades()[0].order == open_order
    assert test_broker_accumulate.get_trades()[0].market_order is False

    assert len(test_broker_accumulate.get_positions()) == 1
    assert test_broker_accumulate.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_accumulate.get_positions()[0].size == 1
    assert test_broker_accumulate.get_positions()[0].avg_bought_price == pytest.approx(
        85.0, abs=0.01
    )
    assert test_broker_accumulate.get_positions()[0].stop_loss is None
    assert test_broker_accumulate.get_positions()[0].take_profit is None

    assert test_broker_accumulate.get_assets_value() == pytest.approx(85.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(15.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 95.0), (None, 95.0, None, None, None)]]
)
def test_open_long_accumulate_on_open_greater_not_opened(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_accumulate: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_accumulate.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_accumulate.process_orders()

    assert len(test_broker_accumulate.get_trades()) == 0
    assert len(test_broker_accumulate.get_positions()) == 0
    assert test_broker_accumulate.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 90.0, 90.0)]])
def test_open_long_distinct_on_close(
    test_market: Market, test_account: Account, test_broker_distinct: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker_distinct.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 85.0, 90.0)]])
def test_open_long_distinct_during_day(
    test_market: Market, test_account: Account, test_broker_distinct: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker_distinct.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 95.0), (None, 90.0, None, None, None)]]
)
def test_open_long_distinct_on_open_equal(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 85.0, None, None, None)]]
)
def test_open_long_distinct_on_open_less(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

    assert len(test_broker_distinct.get_positions()) == 1
    assert test_broker_distinct.get_positions()[0].position_type == PositionType.LONG
    assert test_broker_distinct.get_positions()[0].size == 1
    assert test_broker_distinct.get_positions()[0].avg_bought_price == pytest.approx(
        85.0, abs=0.01
    )
    assert test_broker_distinct.get_positions()[0].stop_loss is None
    assert test_broker_distinct.get_positions()[0].take_profit is None

    assert test_broker_distinct.get_assets_value() == pytest.approx(85.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(15.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 100.0), (None, 95.0, None, None, None)]]
)
def test_open_long_distinct_on_open_greater_not_opened(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 0
    assert len(test_broker_distinct.get_positions()) == 0
    assert test_broker_distinct.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 90.0, 100.0, 90.0, 100.0)]])
def test_open_short_distinct_on_close(
    test_market: Market, test_account: Account, test_broker_distinct: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)
    test_broker_distinct.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

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


@pytest.mark.parametrize("market_data", [[(None, 90.0, 105.0, 90.0, 100.0)]])
def test_open_short_distinct_during_day(
    test_market: Market, test_account: Account, test_broker_distinct: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)
    test_broker_distinct.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

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


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 90.0), (None, 100.0, None, None, None)]]
)
def test_open_short_distinct_on_open_equal(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

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


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 90.0), (None, 100.0, None, None, None)]]
)
def test_open_short_distinct_on_open_less(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=95.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 1
    assert test_broker_distinct.get_trades()[0].order == open_order
    assert test_broker_distinct.get_trades()[0].market_order is False

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


@pytest.mark.parametrize(
    "market_data", [[(None, None, None, None, 90.0), (None, 95.0, None, None, None)]]
)
def test_open_short_distinct_on_open_greater_not_opened(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker_distinct: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker_distinct.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker_distinct.process_orders()

    assert len(test_broker_distinct.get_trades()) == 0
    assert len(test_broker_distinct.get_positions()) == 0
    assert test_broker_distinct.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)
