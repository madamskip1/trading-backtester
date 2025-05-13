from typing import Any

import numpy as np


class Account:
    """Represents the account of the user."""

    def __init__(self, data_size: int, initial_money: float):
        """Initializes an Account object.

        Args:
            data_size (int): The size of the data.
            initial_money (float): The initial amount of user's money.
        """

        self._current_money = initial_money
        self._initial_money = initial_money
        # assets and equity are calculated at the end of the day
        self._assets_value = np.zeros(data_size, dtype=float)
        self._equity = np.zeros(data_size + 1, dtype=float)
        self._equity[0] = initial_money

    def get_current_money(self) -> float:
        """Returns the current amount of money in the account.

        Returns:
            float: The current amount of money in the account.
        """

        return self._current_money

    def get_initial_money(self) -> float:
        """Returns the initial amount of money in the account.

        Returns:
            float: The initial amount of money in the account.
        """

        return self._initial_money

    def calc_return_value(self) -> float:
        """Calculates the return value of the account.

        Returns:
            float: The return value of the account.
        """

        return self.get_final_equity() - self._initial_money

    def get_final_assets_value(self) -> float:
        """Returns the final value of the assets in the account.

        Returns:
            float: The final value of the assets in the account.
        """

        return self._assets_value[-1]

    def get_assets_value(self) -> np.ndarray[Any, np.dtype[Any]]:
        """Returns the value of the assets in the account.

        Returns:
            np.ndarray[Any, np.dtype[Any]]: The value of the assets in the account.
        """

        return self._assets_value

    def get_final_equity(self) -> float:
        """Returns the final equity of the account.

        Returns:
            float: The final equity of the account.
        """

        return self._equity[-1]

    def get_current_equity(self) -> float:
        """Returns the current equity of the account.

        Returns:
            float: The current equity of the account.
        """

        return self._equity[-1] + self._current_money

    def get_equity(self) -> np.ndarray[Any, np.dtype[Any]]:
        """Returns the equity of the account.

        Returns:
            np.ndarray[Any, np.dtype[Any]]: The equity of the account.
        """

        return self._equity

    def update_money(self, amount: float) -> None:
        """Updates the current amount of money in the account.

        Args:
            amount (float): The amount to add or subtract from the current money.
        """

        self._current_money += amount

    def update_assets_value(self, index: int, value: float) -> None:
        """Updates the value of the assets in the account.

        Args:
            index (int): The index of the asset.
            value (float): The value of the asset.
        """

        self._assets_value[index] = value

    def calculate_equity(self, index: int) -> None:
        """Calculates the equity of the account.

        Args:
            index (int): The index of the asset.
        """

        self._equity[index + 1] = self._current_money + self._assets_value[index]

    def has_enough_money(self, amount: float) -> bool:
        """Checks if the account has enough money.

        Args:
            amount (float): The amount to check.

        Returns:
            bool: True if the account has enough money, False otherwise.
        """

        return self._current_money >= amount

    def is_bankrupt(self) -> bool:
        """Checks if the account is bankrupt.

        Returns:
            bool: True if the account is bankrupt, False otherwise.
        """

        return self._current_money <= 0
