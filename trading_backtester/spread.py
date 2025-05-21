class Spread:
    """Represents a spread between the bid and ask prices.

    Spread is applied twice - once at opening and once at closing the position.
    """

    def __init__(self, spread_rate: float):
        """Initialize the Spread object.

        Args:
            spread_rate (float): The spread rate as a fixed amount.
        """

        self.__spread_rate = spread_rate

    def calc_spread_value(self, _: float) -> float:
        """Calculate the spread value.

        Args:
            _ (float): The price of the trade (not used in this case).

        Returns:
            float: The spread value.
        """

        return self.__spread_rate
