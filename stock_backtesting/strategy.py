from .market import Market, MarketTime
from .trade import Trade


class Strategy:
    def __init__(self, market: Market):
        self._market = market

    def check_buy_signal(self, price: float, time: MarketTime) -> bool:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def check_sell_signal(self, price: float, time: MarketTime) -> bool:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def check_close_signal(self, trade: Trade, price: float, time: MarketTime) -> bool:
        raise NotImplementedError("This method should be overridden by subclasses.")
