from enum import Enum
from typing import Any, List, Optional
import numpy as np

BacktestingDataType = np.dtype(
    [("min", "f8"), ("max", "f8"), ("open", "f8"), ("close", "f8")]  # float64
)


class TradeType(Enum):
    LONG = 1
    SHORT = 2


class OpenTradeTime(Enum):
    OPEN = 1
    CLOSE = 2


class CloseTradeTime(Enum):
    OPEN = 1
    CLOSE = 2


class Trade:
    def __init__(self, trade_type: TradeType, size: int, entry_price: float):
        self.trade_type = trade_type
        self.size = size
        self.entry_price = entry_price
        self.exit_price: Optional[float] = None
        self.active = True

    def calc_profit(self) -> float:
        assert self.exit_price

        if self.trade_type == TradeType.LONG:
            return (self.exit_price - self.entry_price) * self.size
        else:
            return (self.entry_price - self.exit_price) * self.size

    def calc_current_value(self, current_price: float) -> float:
        if not self.active:
            return 0.0

        return current_price * self.size


class Account:

    def __init__(self, data_size: int, initial_money: float):
        self.__current_money = initial_money
        # assets and equity are calculated at the end of the day
        self.__assets_value = np.zeros(data_size, dtype=float)
        self.__equity = np.zeros(data_size, dtype=float)

    def get_current_money(self) -> float:
        return self.__current_money

    def get_final_assets_value(self) -> float:
        return self.__assets_value[-1]

    def get_assets_value(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__assets_value

    def get_final_equity(self) -> float:
        return self.__equity[-1]

    def get_equity(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__equity

    def update_money(self, amount: float):
        self.__current_money += amount

    def update_assets_value(self, index: int, value: float):
        self.__assets_value[index] = value

    def calculate_equity(self, index: int):
        self.__equity[index] = self.__current_money + self.__assets_value[index]

    def has_enough_money(self, amount: float) -> bool:
        return self.__current_money >= amount

    def is_bankrupt(self) -> bool:
        return self.__current_money <= 0


class Statistics:

    def __init__(self, trades: List[Trade], account: Account):
        self.__trades = trades
        self.__account = account

    def __str__(self):
        return "\n".join(
            [
                "=== Statistics ===",
                f"Total trades: {len(self.__trades)}",
                f"Total long trades: {len([t for t in self.__trades if t.trade_type == TradeType.LONG])}",
                f"Total short trades: {len([t for t in self.__trades if t.trade_type == TradeType.SHORT])}",
                f"Final money: {self.__account.get_current_money()}",
                f"Final assets value: {self.__account.get_final_assets_value()}",
                f"Final total equity: {self.__account.get_final_equity()}",
            ]
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


if __name__ == "__main__":
    temporary_data = np.array(
        [
            (16.0, 15.0, 18.0, 17.0),
            (4.0, 3.0, 6.0, 5.0),
            (13.0, 12.0, 15.0, 14.0),
            (9.0, 8.0, 11.0, 10.0),
            (6.0, 5.0, 8.0, 7.0),
            (11.0, 10.0, 13.0, 12.0),
            (8.0, 7.0, 10.0, 9.0),
            (2.0, 1.0, 4.0, 3.0),
            (15.0, 14.0, 17.0, 16.0),
            (10.0, 9.0, 12.0, 11.0),
            (7.0, 6.0, 9.0, 8.0),
            (5.0, 4.0, 7.0, 6.0),
            (12.0, 11.0, 14.0, 13.0),
            (14.0, 13.0, 16.0, 15.0),
            (3.0, 2.0, 5.0, 4.0),
        ],
        dtype=BacktestingDataType,
    )
    x = Backtest(
        np.array(temporary_data, dtype=BacktestingDataType),
        open_trade_time=OpenTradeTime.OPEN,
        close_trade_time=CloseTradeTime.CLOSE,
    )
    x.run()
