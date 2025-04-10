from typing import Any, Dict, List, Tuple

from .account import Account
from .trade import Trade, TradeType


class Statistics:

    def __init__(self, trades: List[Trade], account: Account):
        self.__trades = trades
        self.__account = account

    def get_stats(self) -> Dict[str, Any]:
        max_drowdown, max_drawdown_percentage = self.__calc_max_drown()
        return {
            "total_trades": len(self.__trades),
            "total_long_trades": len(
                [t for t in self.__trades if t.trade_type == TradeType.LONG]
            ),
            "total_short_trades": len(
                [t for t in self.__trades if t.trade_type == TradeType.SHORT]
            ),
            "final_money": self.__account.get_current_money(),
            "final_assets_value": self.__account.get_final_assets_value(),
            "final_total_equity": self.__account.get_final_equity(),
            "return": self.__account.calc_return_value(),
            "max_drawdown": max_drowdown,
            "max_drawdown_percentage": max_drawdown_percentage,
        }

    def __str__(self):
        stats = self.get_stats()
        return "\n".join(
            [
                "=== Statistics ===",
                f"Total trades: {stats['total_trades']}",
                f"Total long trades: {stats['total_long_trades']}",
                f"Total short trades: {stats['total_short_trades']}",
                f"Final money: {stats['final_money']}",
                f"Final assets value: {stats['final_assets_value']}",
                f"Final total equity: {stats['final_total_equity']}",
                f"Return: {stats['return']} ({(stats['return'] / self.__account.get_initial_money() * 100):.2f}%)",
                f"Max drawdown: {stats['max_drawdown']} ({stats['max_drawdown_percentage']:.2f}%)",
            ]
        )

    def __calc_max_drown(self) -> Tuple[float, float]:
        max_drawdown = 0.0
        max_drawdown_percentage = 0.0
        peak = self.__account.get_initial_money()

        for equity in self.__account.get_equity():
            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_percentage = (drawdown / peak) * 100

        return max_drawdown, max_drawdown_percentage
