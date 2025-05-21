from enum import Enum


class SpreadType(Enum):
    """Represents the type of spread's calculation."""

    FIXED = 1
    """Fixed spread - a fixed difference between the bid and ask prices."""


class Spread:
    """Represents a spread between the bid and ask prices.

    Spread is applied twice - once at opening and once at closing the position.
    """

    def __init__(self, spread_type: SpreadType, spread_rate: float):
        """Initialize the Spread object.

        Args:
            spread_type (SpreadType): The type of spread's calculation.
            spread_rate (float): The spread rate as a fixed amount.
        """

        self.__spread_type = spread_type
        self.__spread_rate = spread_rate

    def calc_spread_value(self, _: float) -> float:
        """Calculate the spread value.

        Args:
            _ (float): The price of the trade (not used in this case).

        Returns:
            float: The spread value.
        """
        spread = 0.0
        if self.__spread_type == SpreadType.FIXED:
            spread = self.__spread_rate

        return spread
