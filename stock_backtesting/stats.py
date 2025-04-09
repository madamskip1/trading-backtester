from typing import List, Tuple

from .account import Account
from .trade import Trade, TradeType


class Statistics:

    def __init__(self, trades: List[Trade], account: Account):
        self.__trades = trades
        self.__account = account

    def __str__(self):
        max_drowdown, max_drawdown_percentage = self.__calc_max_drown()
        return "\n".join(
            [
                "=== Statistics ===",
                f"Total trades: {len(self.__trades)}",
                f"Total long trades: {len([t for t in self.__trades if t.trade_type == TradeType.LONG])}",
                f"Total short trades: {len([t for t in self.__trades if t.trade_type == TradeType.SHORT])}",
                f"Final money: {self.__account.get_current_money()}",
                f"Final assets value: {self.__account.get_final_assets_value()}",
                f"Final total equity: {self.__account.get_final_equity()}",
                f"Return: {self.__account.calc_return_value()} ({(self.__account.calc_return_value() / self.__account.get_initial_money() * 100):.2f}%)",
                f"Max drawdown: {max_drowdown} ({max_drawdown_percentage:.2f}%)",
            ]
        )

    def __calc_max_drown(self) -> Tuple[float, float]:
        max_drawdown = 0.0
        max_drawdown_percentage = 0.0
        peak = self.__account.get_equity()[0]

        for equity in self.__account.get_equity():
            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_percentage = (drawdown / peak) * 100

        return max_drawdown, max_drawdown_percentage
