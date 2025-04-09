from typing import Any, List, Optional

import numpy as np

from .account import Account
from .stats import Statistics
from .trade import CloseTradeTime, OpenTradeTime, Trade, TradeType

BacktestingDataType = np.dtype(
    [("min", "f8"), ("max", "f8"), ("open", "f8"), ("close", "f8")]
)


class Backtest:
    def __init__(
        self,
        data: np.ndarray[Any, np.dtype[Any]],
        open_trade_time: OpenTradeTime,
        close_trade_time: CloseTradeTime,
    ):
        self.data = data
        self.open_trade_time = open_trade_time
        self.close_trade_time = close_trade_time

        self.current_index = 0
        self.trades: List[Trade] = []

        self.__account = Account(data_size=len(data), initial_money=1000.0)
        self.__statistics = Statistics(self.trades, self.__account)

    def run(self):
        print("Starting backtest...")
        print(f"Data: {self.data}")
        print(f"Initial money: {self.__account.get_current_money()}")

        for i in range(len(self.data)):
            self.current_index = i

            if self.close_trade_time == CloseTradeTime.OPEN:
                self.perform_close_trades()

            if self.open_trade_time == OpenTradeTime.OPEN:
                self.perform_open_trades()

            # Middle of the day

            if self.close_trade_time == CloseTradeTime.CLOSE:
                self.perform_close_trades()

            if self.open_trade_time == OpenTradeTime.CLOSE:
                self.perform_open_trades()

            assets_value = 0.0
            for trade in self.trades:
                if trade.active:
                    assets_value += trade.calc_current_value(
                        self.data[self.current_index]["close"]
                    )

            self.__account.update_assets_value(self.current_index, assets_value)
            self.__account.calculate_equity(self.current_index)

        print("Backtest finished.")

        print(self.__statistics)

    def perform_open_trades(self):
        price_time = "open" if self.open_trade_time == OpenTradeTime.OPEN else "close"
        price = self.data[self.current_index][price_time]

        if self.buy_signal():
            if not self.__account.has_enough_money(price):
                print("Not enough money to buy")
                return

            trade = Trade(TradeType.LONG, 1, price)
            self.trades.append(trade)
            self.__account.update_money(-price)
            print(f"Buy signal at index {self.current_index}: {price}")
            return

        if self.sell_signal():
            if not self.__account.has_enough_money(price):
                print("Not enough money to sell")
                return

            trade = Trade(TradeType.SHORT, 1, price)
            self.trades.append(trade)
            self.__account.update_money(-price)
            print(f"Sell signal at index {self.current_index}: {price}")

    def perform_close_trades(self):
        price_time = "open" if self.close_trade_time == CloseTradeTime.OPEN else "close"
        price = self.data[self.current_index][price_time]
        for trade in self.trades:
            if not trade.active:
                continue

            if self.close_signal(trade):
                if trade.trade_type == TradeType.LONG:
                    trade.active = False
                    trade.exit_price = price
                    self.__account.update_money(trade.calc_current_value(price))
                    print(
                        f"Close long signal at index {self.current_index}: {price}, profit: {trade.calc_profit()}"
                    )
                elif trade.trade_type == TradeType.SHORT:
                    trade.active = False
                    trade.exit_price = price
                    self.__account.update_money(trade.entry_price + trade.calc_profit())
                    print(
                        f"Close short signal at index {self.current_index}: {price}, profit: {trade.calc_profit()}"
                    )

    def get_current_open(self) -> float:
        return self.data[self.current_index]["open"]

    def get_current_close(self) -> float:
        return self.data[self.current_index]["close"]

    def get_previous_open(self) -> Optional[float]:
        if self.current_index > 0:
            return self.data[self.current_index - 1]["open"]
        return None

    def get_previous_close(self) -> Optional[float]:
        if self.current_index > 0:
            return self.data[self.current_index - 1]["close"]
        return None

    def buy_signal(self) -> bool:
        previous_close = self.get_previous_close()
        if previous_close is None:
            return False

        return self.get_current_open() > previous_close

    def sell_signal(self) -> bool:
        previous_close = self.get_previous_close()
        if previous_close is None:
            return False

        return self.get_current_open() < previous_close

    def close_signal(self, trade: Trade) -> bool:
        return True
