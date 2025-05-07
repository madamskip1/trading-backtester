import pytest

from trading_backtester.account import Account
from trading_backtester.broker import Broker
from trading_backtester.data import Data
from trading_backtester.market import Market, MarketTime
from trading_backtester.order import OpenOrder
from trading_backtester.position import PositionType
from trading_backtester.trade import TradeType


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 90.0, 90.0, None)]])
def test_open_long_on_close(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 85.0, 90.0, None)]])
def test_open_long_during_day(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 95.0, None), (None, 90.0, None, None, None, None)]],
)
def test_open_long_on_open_equal(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 95.0, None), (None, 85.0, None, None, None, None)]],
)
def test_open_long_on_open_less(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(85.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        85.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(85.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(15.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 95.0, None), (None, 95.0, None, None, None, None)]],
)
def test_open_long_on_open_greater_not_opened(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 0
    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 90.0, 100.0, 90.0, 100.0, None)]])
def test_open_short_on_close(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(100.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 90.0, 105.0, 90.0, 100.0, None)]])
def test_open_short_during_day(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(100.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 90.0, None), (None, 100.0, None, None, None, None)]],
)
def test_open_short_on_open_equal(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(100.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 90.0, None), (None, 100.0, None, None, None, None)]],
)
def test_open_short_on_open_less(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=95.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(100.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 90.0, None), (None, 95.0, None, None, None, None)]],
)
def test_open_short_on_open_greater_not_opened(
    test_data: Data,
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=100.0)

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order])

    test_data.increment_data_index()
    test_market.set_current_time(MarketTime.OPEN)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 0
    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 100.0, 100.0, 90.0, 90.0, None)], 2.2)]
)
def test_open_long_with_spread_exact_price(
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 0
    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 100.0, 100.0, 87.8, 87.8, None)], 2.2)]
)
def test_open_long_with_spread_enough_price(
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, limit_price=90.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        90.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(87.8, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(10.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 85.0, 95.0, 85.0, 95.0, None)], 2.2)]
)
def test_open_short_with_spread_exact_price(
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=95.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 0
    assert len(test_broker.get_positions()) == 0
    assert test_broker.get_assets_value() == pytest.approx(0.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(100.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 85.0, 97.2, 85.0, 97.2, None)], 2.2)]
)
def test_open_short_with_spread_enough_price(
    test_market: Market,
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, limit_price=95.0)
    test_broker.process_orders([open_order])

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders()

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(95.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is False

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        95.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(92.8, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(5.0, abs=0.01)
