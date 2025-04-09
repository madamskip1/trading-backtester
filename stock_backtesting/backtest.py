from typing import Any, List, Type

import numpy as np

from .account import Account
from .market import Market, MarketTime
from .stats import Statistics
from .strategy import Strategy
from .trade import Trade, TradeType

BacktestingDataType = np.dtype(
    [("min", "f8"), ("max", "f8"), ("open", "f8"), ("close", "f8")]
)


class Backtest:
    def __init__(
        self,
        data: np.ndarray[Any, np.dtype[Any]],
        strategy: Type[Strategy],
    ):
        self.__market = Market(data)
        self.__strategy = strategy(self.__market)
        self.__data_len = len(data)

        self.trades: List[Trade] = []

        self.__account = Account(data_size=len(data), initial_money=1000.0)
        self.__statistics = Statistics(self.trades, self.__account)

    def run(self):
        print("Starting backtest...")
        print(f"Initial money: {self.__account.get_current_money()}")

        for _ in range(self.__data_len):
            self.__market.increment_day()
            self.__market.set_current_time(MarketTime.OPEN)

            self.perform_close_trades()
            self.perform_open_trades()

            self.__market.set_current_time(MarketTime.CLOSE)

            self.perform_close_trades()
            self.perform_open_trades()

            assets_value = 0.0
            for trade in self.trades:
                if trade.active:
                    assets_value += trade.calc_current_value(
                        self.__market.get_today_close_price()
                    )

            self.__account.update_assets_value(
                self.__market.get_current_day(), assets_value
            )
            self.__account.calculate_equity(self.__market.get_current_day())

        print("Backtest finished.")

        print(self.__statistics)

    def perform_open_trades(self):
        price = self.__market.get_current_price()

        if self.__strategy.check_buy_signal(price, self.__market.get_current_time()):
            if not self.__account.has_enough_money(price):
                print("Not enough money to buy")
                return

            trade = Trade(TradeType.LONG, 1, price)
            self.trades.append(trade)
            self.__account.update_money(-price)
            print(f"Buy signal at index {self.__market.get_current_day()}: {price}")
            return

        if self.__strategy.check_sell_signal(price, self.__market.get_current_time()):
            if not self.__account.has_enough_money(price):
                print("Not enough money to sell")
                return

            trade = Trade(TradeType.SHORT, 1, price)
            self.trades.append(trade)
            self.__account.update_money(-price)
            print(f"Sell signal at index {self.__market.get_current_day()}: {price}")

    def perform_close_trades(self):
        price = self.__market.get_current_price()

        for trade in self.trades:
            if not trade.active:
                continue

            if self.__strategy.check_close_signal(
                trade, price, self.__market.get_current_time()
            ):
                if trade.trade_type == TradeType.LONG:
                    trade.active = False
                    trade.exit_price = price
                    self.__account.update_money(trade.calc_current_value(price))
                    print(
                        f"Close long position at index {self.__market.get_current_day()}: {price}, profit: {trade.calc_profit()}"
                    )
                elif trade.trade_type == TradeType.SHORT:
                    trade.active = False
                    trade.exit_price = price
                    self.__account.update_money(trade.entry_price + trade.calc_profit())
                    print(
                        f"Close short position at index {self.__market.get_current_day()}: {price}, profit: {trade.calc_profit()}"
                    )
