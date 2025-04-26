from stock_backtesting.order import Order


class Trade:
    def __init__(self, order: Order, price: float, market_order: bool):
        self.order = order
        self.price = price
        self.market_order = market_order
