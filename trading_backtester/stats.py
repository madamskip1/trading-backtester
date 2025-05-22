from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from trading_backtester.data import Data

from .account import Account
from .position import PositionType
from .trade import Trade, TradeType


class Statistics:
    """Class for calculating and returning backtest statistics.

    This class calculates various statistics related to the backtest,
    including the number of trades, final money, final asset value, final total equity,
    and key indicators such as maximum drawdown, beta, alpha, and the strategy's return.
    """

    @dataclass
    class __TradesCounters:
        total_open_trades: int = 0
        total_close_trades: int = 0
        total_open_long_trades: int = 0
        total_close_long_trades: int = 0
        total_open_short_trades: int = 0
        total_close_short_trades: int = 0

    def __init__(
        self,
        trades: List[Trade],
        equity_log: np.ndarray[Any, np.dtype[Any]],
        account: Account,
        benchmark: Optional[Data] = None,
    ):
        """Initializes the Statistics object.

        Should be used after the backtest is completed.

        Args:
            trades (List[Trade]): List of trades made during the backtest.
            equity_log (np.ndarray): Array containing the equity log of the backtest.
            account (Account): The account used for the backtest.
            benchmark (Optional[Data]): Optional benchmark data for calculating beta and alpha.
        """

        self.__account = account
        self.__trades = trades
        self.__equity_log = equity_log
        self.__benchmark = benchmark

        self.__total_commission = 0.0

    def add_commission(self, commission: float) -> None:
        """Adds the paid commission to the total commission.

        Args:
            commission (float): The commission paid for the trade.
        """

        self.__total_commission += commission

    def get_stats(self) -> Dict[str, Any]:
        """Calculates and returns various statistics related to the backtest.

        Returns:
            Dict[str, Any]: A dictionary containing various statistics related to the backtest.
        """

        max_drowdown, max_drawdown_percentage = self.__calc_max_drown()
        beta = self.__calc_beta()
        trades_counters = self.__get_trades_counters()
        return_value = self.__equity_log[-1] - self.__equity_log[0]
        return_value_percentage = return_value / self.__equity_log[0] * 100

        return {
            "total_trades": len(self.__trades),
            "total_open_trades": trades_counters.total_open_trades,
            "total_close_trades": trades_counters.total_close_trades,
            "total_open_long_trades": trades_counters.total_open_long_trades,
            "total_close_long_trades": trades_counters.total_close_long_trades,
            "total_open_short_trades": trades_counters.total_open_short_trades,
            "total_close_short_trades": trades_counters.total_close_short_trades,
            "final_money": self.__account.current_money,
            "final_assets_value": self.__equity_log[-1] - self.__account.current_money,
            "final_total_equity": self.__equity_log[-1],
            "return": return_value,
            "return_percentage": return_value_percentage,
            "max_drawdown": max_drowdown,
            "max_drawdown_percentage": max_drawdown_percentage,
            "beta": beta,
            "alpha": self.__calc_alpha(beta),
            "total_commission": self.__total_commission,
        }

    def __str__(self) -> str:
        """Returns a string representation of the statistics in a human-readable format.

        Returns:
            str: A string representation of the statistics.
        """

        stats = self.get_stats()
        return "\n".join(
            [
                "=== Statistics ===",
                f"Total trades: {stats['total_trades']}",
                f"Total open trades: {stats['total_open_trades']}",
                f"Total close trades: {stats['total_close_trades']}",
                f"Total open long trades: {stats['total_open_long_trades']}",
                f"Total close long trades: {stats['total_close_long_trades']}",
                f"Total open short trades: {stats['total_open_short_trades']}",
                f"Total close short trades: {stats['total_close_short_trades']}",
                f"Final money: {stats['final_money']}",
                f"Final total equity: {stats['final_total_equity']}",
                f"Return: {stats['return']} ({(stats['return_percentage']):.2f}%)",
                f"Max drawdown: {stats['max_drawdown']} ({stats['max_drawdown_percentage']:.2f}%)",
                f"Beta: {stats['beta']:.2f}",
                f"Alpha: {stats['alpha']:.2f}",
                f"Total commission paid: {stats['total_commission']}",
            ]
        )

    def __calc_max_drown(self) -> Tuple[float, float]:
        max_drawdown = 0.0
        max_drawdown_percentage = 0.0
        peak = self.__equity_log[0]

        for equity in self.__equity_log:
            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_percentage = (drawdown / peak) * 100

        return max_drawdown, max_drawdown_percentage

    def __calc_beta(self) -> Optional[float]:
        if self.__benchmark is None:
            return None

        benchmark_data = np.insert(
            self.__benchmark.close, 0, self.__benchmark.open[0], axis=0
        )
        benchmark_returns = np.diff(benchmark_data) / benchmark_data[:-1]

        equity_returns = np.diff(self.__equity_log) / self.__equity_log[:-1]

        if len(benchmark_returns) < 2 or len(equity_returns) < 2:
            return None

        covariance = np.cov(equity_returns, benchmark_returns)[0, 1]
        market_variance = np.var(benchmark_returns, ddof=1)

        if market_variance == 0:
            return None

        return covariance / market_variance

    def __calc_alpha(
        self, beta: Optional[float], risk_free_rate: float = 0.0
    ) -> Optional[float]:
        if beta is None or self.__benchmark is None:
            return None

        equity_return = (
            self.__equity_log[-1] - self.__equity_log[0]
        ) / self.__equity_log[0]
        benchmark_return = (
            self.__benchmark.close[-1] - self.__benchmark.open[0]
        ) / self.__benchmark.open[0]

        return (
            equity_return - risk_free_rate - beta * (benchmark_return - risk_free_rate)
        )

    def __get_trades_counters(self) -> __TradesCounters:
        counters = self.__TradesCounters()
        for trade in self.__trades:
            if trade.trade_type == TradeType.OPEN:
                counters.total_open_trades += 1
                if trade.position_type == PositionType.LONG:
                    counters.total_open_long_trades += 1
                else:
                    counters.total_open_short_trades += 1
            else:
                counters.total_close_trades += 1
                if trade.position_type == PositionType.LONG:
                    counters.total_close_long_trades += 1
                else:
                    counters.total_close_short_trades += 1

        return counters
