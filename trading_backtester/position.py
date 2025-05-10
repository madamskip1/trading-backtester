from enum import Enum
from typing import Optional

import numpy as np


class PositionType(Enum):
    LONG = 1
    SHORT = 2


class Position:
    def __init__(
        self,
        position_type: PositionType,
        price: float,
        size: int,
        open_dateteime: np.datetime64,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
    ):
        self.position_type = position_type
        self.avg_bought_price = price
        self.size = size
        self.open_datetime = open_dateteime
        self.stop_loss = stop_loss
        self.take_profit = take_profit
