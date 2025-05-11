from typing import List, Tuple

from trading_backtester.account import Account
from trading_backtester.data import Data
from trading_backtester.order import CloseOrder, Order, OrderAction
from trading_backtester.trade import CloseTrade, OpenTrade, Trade

from .position import Position, PositionType


class Broker:
    def __init__(
        self,
        data: Data,
        accout: Account,
        spread: float,
    ):
        self.__data = data
        self.__account = accout
        self.__spread = spread
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
            assets_value += position.calc_value(self.__data.get_current_price())

        return assets_value

    def process_stop_losses(self) -> None:
        low_price = self.__data.get_current_low_price()
        high_price = self.__data.get_current_high_price()

        close_orders: List[Tuple[CloseOrder, float]] = []

        for position in self.__positions:
            if position.stop_loss is None:
                continue

            if not self.__check_stop_loss_price(
                position.stop_loss, low_price, high_price, position.position_type
            ):
                continue

            price = self.__get_stop_loss_order_price(
                position.stop_loss, low_price, high_price, position.position_type
            )

            order = CloseOrder(
                size=position.size,
                position_to_close=position,
            )

            close_orders.append((order, price))

        for order, price in close_orders:
            self.__process_close_order(order, price)

    def process_take_profits(self) -> None:
        low_price = self.__data.get_current_low_price()
        high_price = self.__data.get_current_high_price()

        close_orders: List[Tuple[CloseOrder, float]] = []

        for position in self.__positions:
            if position.take_profit is None:
                continue

            if not self.__check_take_profit_price(
                position.take_profit, low_price, high_price, position.position_type
            ):
                continue

            price = self.__get_take_profit_order_price(
                position.take_profit, low_price, high_price, position.position_type
            )
            order = CloseOrder(
                size=position.size,
                position_to_close=position,
            )

            close_orders.append((order, price))

        for order, price in close_orders:
            self.__process_close_order(order, price)

    def process_orders(self, new_orders: List[Order] = []) -> None:
        price = self.__data.get_current_price()

        for order in new_orders:
            if order.action == OrderAction.CLOSE:
                if order.limit_price is not None:
                    self.__limit_orders.append(order)
                    continue

                adjusted_price = self.__adjust_close_price_by_spread(
                    price, order.position_type
                )
                self.__process_close_order(order, adjusted_price)

        for order in new_orders:
            if order.action == OrderAction.OPEN:
                if order.limit_price is not None:
                    self.__limit_orders.append(order)
                    continue

                adjusted_price = self.__adjust_open_price_by_spread(
                    price, order.position_type
                )
                self.__process_open_order(order, adjusted_price)

        self.__process_limit_orders()

    def __process_limit_orders(self) -> None:
        price = self.__data.get_current_price()
        low_price = self.__data.get_current_low_price()
        high_price = self.__data.get_current_high_price()

        orders_to_remove: List[Order] = []

        for order in self.__limit_orders.copy():
            assert order.limit_price is not None
            if order.action == OrderAction.OPEN:
                if not self.__check_limit_price(
                    order.limit_price, price, order.position_type
                ):
                    continue

                order_price = self.__get_limit_order_price(
                    order.limit_price, low_price, high_price, order.position_type
                )
                self.__process_open_order(order, order_price)
                orders_to_remove.append(order)

        for order in orders_to_remove:
            self.__limit_orders.remove(order)

    def __process_open_order(self, order: Order, price: float) -> None:
        money = order.size * price

        if self.__account.get_current_money() < money:
            return

        self.__positions.append(
            Position(
                order.position_type,
                price,
                self.__data.get_current_numpy_datetime(),
                order.size,
                order.stop_loss,
                order.take_profit,
            )
        )
        self.__account.update_money(-money)

        self.__trades.append(
            OpenTrade(
                order.position_type,
                self.__data.get_current_numpy_datetime(),
                price,
                order.size,
                market_order=(order.limit_price is None),
            )
        )

    def __process_close_order(self, order: Order, price: float) -> None:
        if order.position_to_close is not None:
            if order.size > order.position_to_close.size:
                raise ValueError(
                    "if order.position_to_close is specified, order.size must be less than or equal to order.position_to_close.size"
                )

            self.__account.update_money(
                self.__calc_money_from_close(order.position_to_close, price, order.size)
            )

            if order.size == order.position_to_close.size:
                self.__positions.remove(order.position_to_close)
            else:
                position_index = self.__positions.index(order.position_to_close)
                self.__positions[position_index] = order.position_to_close.replace(
                    size=order.position_to_close.size - order.size
                )

            self.__trades.append(
                CloseTrade(
                    order.position_type,
                    order.position_to_close.open_datetime,
                    order.position_to_close.open_price,
                    self.__data.get_current_numpy_datetime(),
                    price,
                    order.size,
                    market_order=(order.limit_price is None),
                )
            )
        else:
            size_to_reduce_left = order.size
            positions_to_close: List[Position] = []
            for i, position in enumerate(self.__positions):
                if position.position_type != order.position_type:
                    continue

                reduce_size = min(size_to_reduce_left, position.size)

                if reduce_size < position.size:
                    self.__account.update_money(
                        self.__calc_money_from_close(position, price, reduce_size)
                    )
                    self.__positions[i] = position.replace(
                        size=position.size - reduce_size
                    )
                else:
                    self.__account.update_money(
                        self.__calc_money_from_close(position, price, reduce_size)
                    )
                    positions_to_close.append(position)

                size_to_reduce_left -= reduce_size

                self.__trades.append(
                    CloseTrade(
                        order.position_type,
                        position.open_datetime,
                        position.open_price,
                        self.__data.get_current_numpy_datetime(),
                        price,
                        reduce_size,
                        market_order=(order.limit_price is None),
                    )
                )
                if size_to_reduce_left == 0:
                    break

            for position in positions_to_close:
                self.__positions.remove(position)

    def __adjust_open_price_by_spread(
        self, price: float, position_type: PositionType
    ) -> float:
        return (
            price + self.__spread
            if position_type == PositionType.LONG
            else price - self.__spread
        )

    def __adjust_close_price_by_spread(
        self, price: float, position_type: PositionType
    ) -> float:
        return (
            price - self.__spread
            if position_type == PositionType.LONG
            else price + self.__spread
        )

    def __calc_money_from_close(
        self, position: Position, current_price: float, size: int
    ) -> float:
        return (
            size * current_price
            if position.position_type == PositionType.LONG
            else size * (2 * position.open_price - current_price)
        )

    def __check_limit_price(
        self, limit_price: float, price: float, position_type: PositionType
    ) -> bool:
        price = self.__adjust_open_price_by_spread(price, position_type)
        return (
            limit_price >= price
            if position_type == PositionType.LONG
            else limit_price <= price
        )

    def __get_limit_order_price(
        self,
        limit_price: float,
        low_price: float,
        high_price: float,
        position_type: PositionType,
    ) -> float:
        return (
            min(high_price, limit_price)
            if position_type == PositionType.LONG
            else max(low_price, limit_price)
        )

    def __check_stop_loss_price(
        self,
        stop_loss_price: float,
        low_price: float,
        high_price: float,
        position_type: PositionType,
    ) -> bool:
        adjusted_low_price = self.__adjust_close_price_by_spread(
            low_price, position_type
        )
        adjusted_high_price = self.__adjust_close_price_by_spread(
            high_price, position_type
        )

        return (
            stop_loss_price >= adjusted_low_price
            if position_type == PositionType.LONG
            else stop_loss_price <= adjusted_high_price
        )

    def __get_stop_loss_order_price(
        self,
        stop_loss_price: float,
        low_price: float,
        high_price: float,
        position_type: PositionType,
    ) -> float:
        return (
            min(high_price, stop_loss_price)
            if position_type == PositionType.LONG
            else max(low_price, stop_loss_price)
        )

    def __check_take_profit_price(
        self,
        take_profit_price: float,
        low_price: float,
        high_price: float,
        position_type: PositionType,
    ) -> bool:
        adjusted_low_price = self.__adjust_close_price_by_spread(
            low_price, position_type
        )
        adjusted_high_price = self.__adjust_close_price_by_spread(
            high_price, position_type
        )

        return (
            take_profit_price <= adjusted_high_price
            if position_type == PositionType.LONG
            else take_profit_price >= adjusted_low_price
        )

    def __get_take_profit_order_price(
        self,
        take_profit_price: float,
        low_price: float,
        high_price: float,
        position_type: PositionType,
    ) -> float:
        return (
            max(low_price, take_profit_price)
            if position_type == PositionType.LONG
            else min(high_price, take_profit_price)
        )
