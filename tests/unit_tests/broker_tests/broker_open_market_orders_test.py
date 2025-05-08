import pytest

from trading_backtester.account import Account
from trading_backtester.broker import Broker
from trading_backtester.market import Market, MarketTime
from trading_backtester.order import OpenOrder
from trading_backtester.position import PositionType
from trading_backtester.trade import TradeType


@pytest.mark.parametrize("market_data", [[(None, 100.0, None, None, None)]])
def test_open_long_single(test_account: Account, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )
    test_broker.process_orders([open_order])

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        100.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(100.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, None)]])
def test_open_long_multiple_in_single_process(
    test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    open_order2 = OpenOrder(
        size=2,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order1, open_order2])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(25.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(25.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size == 2
    assert test_broker.get_trades()[1].close_price is None
    assert test_broker.get_trades()[1].close_size is None
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 2
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None
    assert test_broker.get_positions()[1].position_type == PositionType.LONG
    assert test_broker.get_positions()[1].size == 2
    assert test_broker.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[1].stop_loss is None
    assert test_broker.get_positions()[1].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(25.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 25.0)]])
def test_open_long_multiple_in_multiple_processes(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_broker.process_orders([open_order1])

    open_order2 = OpenOrder(
        size=2,
        position_type=PositionType.LONG,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order2])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(50.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(25.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size == 2
    assert test_broker.get_trades()[1].close_price is None
    assert test_broker.get_trades()[1].close_size is None
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 2
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None
    assert test_broker.get_positions()[1].position_type == PositionType.LONG
    assert test_broker.get_positions()[1].size == 2
    assert test_broker.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )
    assert test_broker.get_positions()[1].stop_loss is None
    assert test_broker.get_positions()[1].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, None, None, None)]])
def test_open_short_single(test_account: Account, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order])

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True

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


@pytest.mark.parametrize("market_data", [[(None, 25.0, None, None, None)]])
def test_open_short_multiple_in_single_process(
    test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    open_order2 = OpenOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order1, open_order2])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(25.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(25.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size == 2
    assert test_broker.get_trades()[1].close_price is None
    assert test_broker.get_trades()[1].close_size is None
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 2
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker.get_positions()[1].position_type == PositionType.SHORT
    assert test_broker.get_positions()[1].size == 2
    assert test_broker.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker.get_assets_value() == pytest.approx(75.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(25.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, None, None, 25.0)]])
def test_open_short_multiple_in_multiple_processes(
    test_market: Market, test_account: Account, test_broker: Broker
):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_broker.process_orders([open_order1])

    open_order2 = OpenOrder(
        size=2,
        position_type=PositionType.SHORT,
    )

    test_market.set_current_time(MarketTime.CLOSE)
    test_broker.process_orders([open_order2])

    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(50.0, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True
    assert test_broker.get_trades()[1].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(25.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size == 2
    assert test_broker.get_trades()[1].close_price is None
    assert test_broker.get_trades()[1].close_size is None
    assert test_broker.get_trades()[1].market_order is True

    assert len(test_broker.get_positions()) == 2
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        50.0, abs=0.01
    )

    assert test_broker.get_positions()[1].position_type == PositionType.SHORT
    assert test_broker.get_positions()[1].size == 2
    assert test_broker.get_positions()[1].avg_bought_price == pytest.approx(
        25.0, abs=0.01
    )

    assert test_broker.get_assets_value() == pytest.approx(125.0, abs=0.01)

    assert test_account.get_current_money() == pytest.approx(0.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, None, None, None)], 2.2)]
)
def test_open_long_with_spread(
    test_account: Account,
    test_broker: Broker,
    # spread: float
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )
    test_broker.process_orders([open_order])

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.LONG
    assert test_broker.get_trades()[0].open_price == pytest.approx(92.2, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.LONG
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        92.2, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(90.0, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(7.8, abs=0.01)


@pytest.mark.parametrize(
    "market_data, spread", [([(None, 90.0, None, None, None)], 2.2)]
)
def test_open_short_with_spread(
    test_account: Account,
    test_broker: Broker,
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )
    test_broker.process_orders([open_order])

    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_trades()[0].trade_type == TradeType.OPEN
    assert test_broker.get_trades()[0].position_type == PositionType.SHORT
    assert test_broker.get_trades()[0].open_price == pytest.approx(87.8, abs=0.01)
    assert test_broker.get_trades()[0].open_size == 1
    assert test_broker.get_trades()[0].close_price is None
    assert test_broker.get_trades()[0].close_size is None
    assert test_broker.get_trades()[0].market_order is True

    assert len(test_broker.get_positions()) == 1
    assert test_broker.get_positions()[0].position_type == PositionType.SHORT
    assert test_broker.get_positions()[0].size == 1
    assert test_broker.get_positions()[0].avg_bought_price == pytest.approx(
        87.8, abs=0.01
    )
    assert test_broker.get_positions()[0].stop_loss is None
    assert test_broker.get_positions()[0].take_profit is None

    assert test_broker.get_assets_value() == pytest.approx(85.6, abs=0.01)
    assert test_account.get_current_money() == pytest.approx(12.2, abs=0.01)
