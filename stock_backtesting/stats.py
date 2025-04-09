from typing import List

from .account import Account
from .trade import Trade, TradeType


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
