from stock_backtesting.order import Order


class Trade:
    def __init__(self, order: Order, price: float, date_index: int):
        self.order = order
        self.price = price
        self.date_index = date_index
