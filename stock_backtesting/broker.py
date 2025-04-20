from typing import List

from stock_backtesting.account import Account
from stock_backtesting.market import Market
from stock_backtesting.order import Order, OrderAction, OrderType
from stock_backtesting.trade import Trade

from .position import Position, PositionMode, PositionType


class Broker:
    def __init__(
        self,
        position_mode: PositionMode,
        market: Market,
        accout: Account,
    ):
        self.__position_mode = position_mode
        self.__market = market
        self.__account = accout
        self.__positions: List[Position] = []
        self.__trades: List[Trade] = []

    def get_trades(self) -> List[Trade]:
        return self.__trades

    def get_positions(self) -> List[Position]:
        return self.__positions

    def get_assets_value(self) -> float:
        assets_value = 0.0
        for position in self.__positions:
            if position.position_type == PositionType.LONG:
                assets_value += position.size * self.__market.get_current_price()
            elif position.position_type == PositionType.SHORT:
                assets_value += position.size * (
                    2 * position.avg_bought_price - self.__market.get_current_price()
                )

        return assets_value

    def process_stop_losses(self) -> None:
        min_price = self.__market.get_current_session_min_price()
        max_price = self.__market.get_current_session_max_price()

        for position in self.__positions:
            if position.stop_loss is None:
                continue
            if position.position_type == PositionType.LONG:
                print(position.stop_loss, min_price)
                if position.stop_loss >= min_price:
                    order = Order(
                        order_type=OrderType.MARKET_ORDER,
                        size=position.size,
                        action=OrderAction.CLOSE,
                        position_to_close=position,
                    )
                    print(max_price, position.stop_loss)
                    price = min(max_price, position.stop_loss)
                    print(price)
                    self.__process_close_order(order, price)

            elif position.position_type == PositionType.SHORT:
                if position.stop_loss <= max_price:
                    order = Order(
                        order_type=OrderType.MARKET_ORDER,
                        size=position.size,
                        action=OrderAction.CLOSE,
                        position_to_close=position,
                    )

                    price = max(min_price, position.stop_loss)
                    self.__process_close_order(order, price)

    def process_take_profits(self) -> None:
        min_price = self.__market.get_current_session_min_price()
        max_price = self.__market.get_current_session_max_price()

        for position in self.__positions:
            if position.take_profit is None:
                continue
            if position.position_type == PositionType.LONG:
                if position.take_profit <= max_price:
                    order = Order(
                        order_type=OrderType.MARKET_ORDER,
                        size=position.size,
                        action=OrderAction.CLOSE,
                        position_to_close=position,
                    )

                    price = max(min_price, position.take_profit)
                    self.__process_close_order(order, price)

            elif position.position_type == PositionType.SHORT:
                if position.take_profit >= self.__market.get_current_price():
                    order = Order(
                        order_type=OrderType.MARKET_ORDER,
                        size=position.size,
                        action=OrderAction.CLOSE,
                        position_to_close=position,
                    )

                    price = min(max_price, position.take_profit)
                    self.__process_close_order(order, price)

    def process_open_orders(self, orders: List[Order]) -> None:
        for order in orders:
            if order.action != OrderAction.OPEN:
                continue

            money = order.size * self.__market.get_current_price()
            if self.__account.get_current_money() < money:
                continue

            if self.__position_mode == PositionMode.ACCUMULATE:
                if order.position_type == PositionType.SHORT:
                    raise ValueError("Cannot open short position in accumulate mode")

                if len(self.__positions) == 0:
                    self.__positions.append(Position(PositionType.LONG))
                self.__accumulate(
                    self.__positions[0], self.__market.get_current_price(), order.size
                )
                self.__positions[0].stop_loss = order.stop_loss
                self.__positions[0].take_profit = order.take_profit
                self.__account.update_money(-money)
                order.position_type = PositionType.LONG
            elif self.__position_mode == PositionMode.DISTINCT:
                if order.position_type is None:
                    raise ValueError("Order must has position_type in distinct mode")

                self.__positions.append(
                    Position(
                        order.position_type,
                        self.__market.get_current_price(),
                        order.size,
                        order.stop_loss,
                        order.take_profit,
                    )
                )
                self.__account.update_money(-money)

            self.__trades.append(
                Trade(
                    order,
                    self.__market.get_current_price(),
                    self.__market.get_current_day(),
                )
            )

    def process_close_orders(self, orders: List[Order]) -> None:
        for order in orders:
            if order.action != OrderAction.CLOSE:
                continue

            self.__process_close_order(order, self.__market.get_current_price())

    def __process_close_order(self, order: Order, price: float) -> None:
        if self.__position_mode == PositionMode.ACCUMULATE:
            self.__reduce(self.__positions[0], order.size)
            money = order.size * price
            self.__account.update_money(money)
            order.position_type = PositionType.LONG
        elif self.__position_mode == PositionMode.DISTINCT:
            if order.position_to_close is None:
                raise ValueError("Order must has position_to_close in distinct mode")

            if order.position_to_close.position_type == PositionType.LONG:
                self.__reduce(order.position_to_close, order.size)
                money = order.size * price
                self.__account.update_money(money)
            elif order.position_to_close.position_type == PositionType.SHORT:
                self.__reduce(order.position_to_close, order.size)
                money = order.size * (
                    2 * order.position_to_close.avg_bought_price - price
                )
                self.__account.update_money(money)

            order.position_type = order.position_to_close.position_type

        self.__trades.append(
            Trade(
                order,
                price,
                self.__market.get_current_day(),
            )
        )

    def __accumulate(self, position: Position, price: float, size: int) -> None:
        position.avg_bought_price = (
            position.avg_bought_price * position.size + price * size
        ) / (position.size + size)
        position.size += size

    def __reduce(self, position: Position, size: int) -> None:
        position.size -= size
        if position.size == 0:
            self.__positions.remove(position)
