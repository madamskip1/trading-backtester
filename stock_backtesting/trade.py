from enum import Enum
from typing import Optional

from stock_backtesting.order import Order


class Trade:
    def __init__(self, order: Order, date_index: int):
        self.order = order
        self.date_index = date_index
