from typing import List

from stock_backtesting.account import Account
from stock_backtesting.market import Market
from stock_backtesting.order import CloseOrder, Order, OrderAction
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
        self.__limit_orders: List[Order] = []

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
                    order = CloseOrder(
                        size=position.size,
                        position_to_close=position,
                    )
                    print(max_price, position.stop_loss)
                    price = min(max_price, position.stop_loss)
                    print(price)
                    self.__process_close_order(order, price)

            elif position.position_type == PositionType.SHORT:
                if position.stop_loss <= max_price:
                    order = CloseOrder(
                        size=position.size,
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
                    order = CloseOrder(
                        size=position.size,
                        position_to_close=position,
                    )

                    price = max(min_price, position.take_profit)
                    self.__process_close_order(order, price)

            elif position.position_type == PositionType.SHORT:
                if position.take_profit >= self.__market.get_current_price():
                    order = CloseOrder(
                        size=position.size,
                        position_to_close=position,
                    )

                    price = min(max_price, position.take_profit)
                    self.__process_close_order(order, price)

    def process_orders(self, new_orders: List[Order] = []) -> None:
        price = self.__market.get_current_price()

        for order in new_orders:
            if order.action == OrderAction.CLOSE:
                if order.limit_price is not None:
                    self.__limit_orders.append(order)
                    continue
                self.__process_close_order(order, price)

        for order in new_orders:
            if order.action == OrderAction.OPEN:
                if order.limit_price is not None:
                    self.__limit_orders.append(order)
                    continue
                self.__process_open_order(order, price)

        self.__process_limit_orders()

    def __process_limit_orders(self) -> None:
        price = self.__market.get_current_price()
        min_price = self.__market.get_current_session_min_price()
        max_price = self.__market.get_current_session_max_price()

        for order in self.__limit_orders:
            assert order.limit_price is not None
            if order.action == OrderAction.OPEN:
                if not self.__check_limit_price(
                    order.limit_price, price, order.position_type
                ):
                    continue

                order_price = self.__get_limit_order_price(
                    order.limit_price, min_price, max_price, order.position_type
                )
                self.__process_open_order(order, order_price)
                self.__limit_orders.remove(order)

    def __process_open_order(self, order: Order, price: float) -> None:
        money = order.size * price
        if self.__account.get_current_money() < money:
            return

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
                market_order=(order.limit_price is None),
                date_index=self.__market.get_current_day(),
            )
        )

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
                market_order=(order.limit_price is None),
                date_index=self.__market.get_current_day(),
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

    def __check_limit_price(
        self, limit_price: float, price: float, position_type: PositionType
    ) -> bool:
        return (
            limit_price >= price
            if position_type == PositionType.LONG
            else limit_price <= price
        )

    def __get_limit_order_price(
        self,
        limit_price: float,
        min_price: float,
        max_price: float,
        position_type: PositionType,
    ) -> float:
        return (
            min(max_price, limit_price)
            if position_type == PositionType.LONG
            else max(min_price, limit_price)
        )
