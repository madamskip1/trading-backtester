import numpy as np

from stock_backtesting.backtest import Backtest, BacktestingDataType
from stock_backtesting.trade import CloseTradeTime, OpenTradeTime

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
