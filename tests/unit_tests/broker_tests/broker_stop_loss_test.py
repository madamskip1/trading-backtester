import pytest

from trading_backtester.account import Account
from trading_backtester.broker import Broker
from trading_backtester.commission import CommissionType
from trading_backtester.data import CandlestickPhase, Data
from trading_backtester.order import OpenOrder
from trading_backtester.position import PositionType
from trading_backtester.trade import TradeType


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 100.0, None), (None, 99.0, None, None, None, None)]],
)
def test_long_equal_on_open_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=99.0,
    )
    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_new_orders([open_order])

    test_data.increment_data_index()
    test_data.set_candlestick_phase(CandlestickPhase.OPEN)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(99.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 100.0, None), (None, 98.0, None, None, None, None)]],
)
def test_long_greater_on_open_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=99.0,
    )

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_new_orders([open_order])

    test_data.increment_data_index()
    test_data.set_candlestick_phase(CandlestickPhase.OPEN)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(98.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 100.0, None), (None, 99.5, None, None, None, None)]],
)
def test_long_less_on_open_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=99.0,
    )

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_new_orders([open_order])

    test_data.increment_data_index()
    test_data.set_candlestick_phase(CandlestickPhase.OPEN)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(99.5, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 99.0, 99.0, None)]])
def test_long_on_close_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=99.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(99.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 98.0, 99.5, None)]])
def test_long_during_day(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=99.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(99.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 99.1, 99.5, None)]])
def test_long_not_happend_during_day(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=99.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(99.5, abs=0.01)


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 100.0, None), (None, 101.0, None, None, None, None)]],
)
def test_short_equal_on_open_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=101.0,
    )

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_new_orders([open_order])

    test_data.increment_data_index()
    test_data.set_candlestick_phase(CandlestickPhase.OPEN)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 100.0, None), (None, 102.0, None, None, None, None)]],
)
def test_short_less_on_open_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=101.0,
    )

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_new_orders([open_order])

    test_data.increment_data_index()
    test_data.set_candlestick_phase(CandlestickPhase.OPEN)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_assets_value() == 0

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(102.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data",
    [[(None, None, None, None, 100.0, None), (None, 100.5, None, None, None, None)]],
)
def test_short_greater_on_open_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=101.0,
    )

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_new_orders([open_order])

    test_data.increment_data_index()
    test_data.set_candlestick_phase(CandlestickPhase.OPEN)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(99.5, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 100.0, 101.0, None)]])
def test_short_equal_on_close_time(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=101.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 100.0, 100.5, None)]])
def test_short_equal_during_day(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=101.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.9, 100.0, 100.5, None)]])
def test_short_equal_not_happend_during_day(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=101.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(99.5, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 100.0, 99.0, 99.0, None)]])
def test_stop_loss_not_set_long(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(99.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 100.0, 101.0, 100.0, 101.0, None)]])
def test_stop_loss_not_set_short(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 1
    assert test_broker.get_assets_value() == pytest.approx(99.0, abs=0.01)


@pytest.mark.parametrize("market_data", [[(None, 50.0, 50.0, 49.0, 49.0, None)]])
def test_multiple_long_positions(test_data: Data, test_broker: Broker):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=49.0,
    )

    open_order2 = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=48.0,
    )

    test_broker.process_new_orders([open_order1, open_order2])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 3

    assert test_broker.get_trades()[2].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[2].position_type == PositionType.LONG
    assert test_broker.get_trades()[2].open_price == pytest.approx(50.0, abs=0.01)
    assert test_broker.get_trades()[2].open_size is None
    assert test_broker.get_trades()[2].close_price == pytest.approx(49.0, abs=0.01)
    assert test_broker.get_trades()[2].close_size == 1
    assert test_broker.get_trades()[2].market_order is True


@pytest.mark.parametrize("market_data", [[(None, 50.0, 51.0, 50.0, 51.0, None)]])
def test_multiple_short_positions(test_data: Data, test_broker: Broker):
    open_order1 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=51.0,
    )

    open_order2 = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=52.0,
    )

    test_broker.process_new_orders([open_order1, open_order2])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1
    assert len(test_broker.get_trades()) == 3
    assert test_broker.get_assets_value() == pytest.approx(49.0, abs=0.01)

    assert test_broker.get_trades()[2].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[2].position_type == PositionType.SHORT
    assert test_broker.get_trades()[2].open_price == pytest.approx(50.0, abs=0.01)
    assert test_broker.get_trades()[2].open_size is None
    assert test_broker.get_trades()[2].close_price == pytest.approx(51.0, abs=0.01)
    assert test_broker.get_trades()[2].close_size == 1
    assert test_broker.get_trades()[2].market_order is True


@pytest.mark.parametrize(
    "market_data, spread_rate", [([(None, 90.0, 90.0, 80.0, 80.0, None)], 2.2)]
)
def test_long_with_spread_exact_price(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, stop_loss=80.0)
    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(92.2, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data, spread_rate", [([(None, 90.0, 90.0, 82.2, 82.2, None)], 2.2)]
)
def test_long_with_spread_enough_price(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(size=1, position_type=PositionType.LONG, stop_loss=80.0)
    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(92.2, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data, spread_rate", [([(None, 80.0, 90.0, 80.0, 90.0, None)], 2.2)]
)
def test_short_with_spread_exact_price(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, stop_loss=90.0)
    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(77.8, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data, spread_rate", [([(None, 80.0, 88.8, 80.0, 88.8, None)], 2.2)]
)
def test_short_with_spread_enough_price(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(size=1, position_type=PositionType.SHORT, stop_loss=90.0)
    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(77.8, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data",
    [[(None, 100.0, 100.0, 99.0, 99.0, None), (None, 99.0, 99.0, 99.0, 99.0, None)]],
)
def test_long_stop_loss_update(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=98.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1

    test_broker.get_positions()[0].update_stop_loss(99.0)

    test_data.increment_data_index()
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(99.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data",
    [
        [
            (None, 100.0, 100.0, 101.0, 101.0, None),
            (None, 101.0, 101.0, 101.0, 101.0, None),
        ]
    ],
)
def test_short_stop_loss_update(test_data: Data, test_broker: Broker):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=102.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 1

    test_broker.get_positions()[0].update_stop_loss(101.0)

    test_data.increment_data_index()
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2

    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(100.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(101.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [([(None, 90.0, 90.0, 80.0, 80.0, None)], 0.02, CommissionType.RELATIVE)],
)
def test_long_relative_commission(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=80.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(86.6, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [([(None, 80.0, 90.0, 80.0, 90.0, None)], 0.02, CommissionType.RELATIVE)],
)
def test_short_relative_commission(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=90.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(86.6, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type, spread_rate",
    [([(None, 90.0, 90.0, 80.0, 80.0, None)], 0.02, CommissionType.RELATIVE, 2.2)],
)
def test_long_commission_and_spread(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=80.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(92.2, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(84.36, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type, spread_rate",
    [([(None, 80.0, 90.0, 80.0, 90.0, None)], 0.02, CommissionType.RELATIVE, 2.2)],
)
def test_short_commission_and_spread(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=90.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(77.8, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(84.44, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [
        (
            [(None, 90.0, 90.0, 80.0, 80.0, None)],
            (5.0, 0.02),
            CommissionType.MINIMUM_RELATIVE,
        )
    ],
)
def test_long_minimum_commission_less(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=80.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(80.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [
        (
            [(None, 90.0, 90.0, 80.0, 80.0, None)],
            (1.0, 0.02),
            CommissionType.MINIMUM_RELATIVE,
        )
    ],
)
def test_long_minimum_commission_greater(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=80.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(86.6, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [
        (
            [(None, 80.0, 90.0, 80.0, 90.0, None)],
            (1.0, 0.02),
            CommissionType.MINIMUM_RELATIVE,
        )
    ],
)
def test_short_minimum_commission_greater(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=90.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(86.6, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [
        (
            [(None, 80.0, 90.0, 80.0, 90.0, None)],
            (5.0, 0.02),
            CommissionType.MINIMUM_RELATIVE,
        )
    ],
)
def test_short_minimum_commission_less(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=90.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(80.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [
        (
            [(None, 90.0, 90.0, 80.0, 80.0, None)],
            5.0,
            CommissionType.FIXED,
        )
    ],
)
def test_long_fixed_commission(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.LONG,
        stop_loss=80.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.LONG
    assert test_broker.get_trades()[1].open_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(80.0, abs=0.01)


@pytest.mark.parametrize(
    "market_data, commission_rate, commission_type",
    [
        (
            [(None, 80.0, 90.0, 80.0, 90.0, None)],
            5.0,
            CommissionType.FIXED,
        )
    ],
)
def test_short_fixed_commission(
    test_data: Data, test_broker: Broker, test_account: Account
):
    open_order = OpenOrder(
        size=1,
        position_type=PositionType.SHORT,
        stop_loss=90.0,
    )

    test_broker.process_new_orders([open_order])

    test_data.set_candlestick_phase(CandlestickPhase.CLOSE)
    test_broker.process_stop_losses()

    assert len(test_broker.get_positions()) == 0
    assert len(test_broker.get_trades()) == 2
    assert test_broker.get_trades()[1].trade_type == TradeType.CLOSE
    assert test_broker.get_trades()[1].position_type == PositionType.SHORT
    assert test_broker.get_trades()[1].open_price == pytest.approx(80.0, abs=0.01)
    assert test_broker.get_trades()[1].open_size is None
    assert test_broker.get_trades()[1].close_price == pytest.approx(90.0, abs=0.01)
    assert test_broker.get_trades()[1].close_size == 1
    assert test_broker.get_trades()[1].market_order is True

    assert test_broker.get_assets_value() == 0
    assert test_account.current_money == pytest.approx(80.0, abs=0.01)
