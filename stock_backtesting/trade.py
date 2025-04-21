from stock_backtesting.order import Order


class Trade:
    def __init__(self, order: Order, price: float, market_order: bool, date_index: int):
        self.order = order
        self.price = price
        self.date_index = date_index
        self.market_order = market_order
