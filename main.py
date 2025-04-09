import numpy as np

from stock_backtesting.backtest import Backtest, BacktestingDataType
from stock_backtesting.market import MarketTime
from stock_backtesting.strategy import Strategy
from stock_backtesting.trade import Trade


class BuyOnOpenSellOnCloseStrategy(Strategy):

    def check_buy_signal(self, price: float, time: MarketTime) -> bool:
        return time == MarketTime.OPEN

    def check_sell_signal(self, price: float, time: MarketTime) -> bool:
        pass

    def check_close_signal(self, trade: Trade, price: float, time: MarketTime) -> bool:
        return time == MarketTime.CLOSE


if __name__ == "__main__":
    temporary_data = np.array(
        [
            (16.0, 15.0, 18.0, 17.0),
            (4.0, 3.0, 5.0, 6.0),
            (13.0, 12.0, 14.0, 15.0),
            (9.0, 8.0, 11.0, 10.0),
            (6.0, 5.0, 8.0, 7.0),
            (11.0, 10.0, 11.0, 12.0),
            (8.0, 7.0, 8.0, 9.0),
            (2.0, 1.0, 4.0, 3.0),
            (15.0, 14.0, 17.0, 16.0),
            (10.0, 9.0, 12.0, 11.0),
            (7.0, 6.0, 5.0, 8.0),
            (5.0, 4.0, 7.0, 6.0),
            (12.0, 11.0, 5.0, 13.0),
            (14.0, 13.0, 16.0, 15.0),
            (3.0, 2.0, 5.0, 4.0),
        ],
        dtype=BacktestingDataType,
    )
    x = Backtest(
        np.array(temporary_data, dtype=BacktestingDataType),
        BuyOnOpenSellOnCloseStrategy,
    )
    x.run()
