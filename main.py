from enum import Enum
from typing import Any, List, Optional
import numpy as np

BacktestingDataType = np.dtype(
    [("min", "f8"), ("max", "f8"), ("open", "f8"), ("close", "f8")]  # float64
)


class TradeType(Enum):
    LONG = 1
    SHORT = 2


class Trade:
    def __init__(self, trade_type: TradeType, size: int, entry_price: float):
        self.trade_type = trade_type
        self.size = size
        self.entry_price = entry_price
        self.exit_price: Optional[float] = None
        self.active = True

    def calc_profit(self) -> Optional[float]:
        if self.exit_price is None:
            return None
        if self.trade_type == TradeType.LONG:
            return (self.exit_price - self.entry_price) * self.size
        else:
            return (self.entry_price - self.exit_price) * self.size


class Backtest:
    def __init__(self, data: np.ndarray[Any, np.dtype[Any]]):
        self.data = data
        self.current_index = 0

        self.money = 1000
        self.trades: List[Trade] = []

    def run(self):
        print("Starting backtest...")
        print(f"Data: {self.data}")
        print(f"Initial money: {self.money}")

        for i, row in enumerate(self.data):
            self.current_index = i

            for trade in self.trades:
                if not trade.active:
                    continue

                # For now, we can sell at least on next day
                if self.close_signal(trade):
                    trade.active = False
                    trade.exit_price = row["close"]
                    self.money += row["close"] * trade.size
                    print(
                        f"Close signal at index {i}: {row['close']}, profit: {trade.calc_profit()}"
                    )

            if self.buy_signal():
                if self.money < row["open"]:
                    print("Not enough money to buy")
                    continue

                trade = Trade(TradeType.LONG, 1, row["open"])
                self.trades.append(trade)
                self.money -= row["open"]
                print(f"Buy signal at index {i}: {row["open"]}")

        print("Backtest finished.")
        print(f"Final money: {self.money}")

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
    x = Backtest(np.array(temporary_data, dtype=BacktestingDataType))
    x.run()
