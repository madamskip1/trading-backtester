from typing import Any

import numpy as np


class Account:

    def __init__(self, data_size: int, initial_money: float):
        self._current_money = initial_money
        self._initial_money = initial_money
        # assets and equity are calculated at the end of the day
        self._assets_value = np.zeros(data_size, dtype=float)
        self._equity = np.zeros(data_size, dtype=float)

    def get_current_money(self) -> float:
        return self._current_money

    def get_initial_money(self) -> float:
        return self._initial_money

    def calc_return_value(self) -> float:
        return self.get_final_equity() - self._initial_money

    def get_final_assets_value(self) -> float:
        return self._assets_value[-1]

    def get_assets_value(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self._assets_value

    def get_final_equity(self) -> float:
        return self._equity[-1]

    def get_equity(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self._equity

    def update_money(self, amount: float):
        self._current_money += amount

    def update_assets_value(self, index: int, value: float):
        self._assets_value[index] = value

    def calculate_equity(self, index: int):
        self._equity[index] = self._current_money + self._assets_value[index]

    def has_enough_money(self, amount: float) -> bool:
        return self._current_money >= amount

    def is_bankrupt(self) -> bool:
        return self._current_money <= 0
