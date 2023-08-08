from collections import defaultdict
from share_prices import StockPrice, StockPrices


class StockPortfolio:
    def __init__(self, prices: StockPrices):
        self.shares = defaultdict(int)
        self.prices = prices

    def get_full_value(self) -> float:
        return sum(
            self.prices.get_actual_price(i) for i in self.shares
        )  # is this correct?

    def update_portfolio(self):
        pass

    def clean_zero_stock(self):
        for key in self.shares:
            if self.shares[key] <= 0:
                del self.shares[key]

    def buy(self, available_cash, num_shares=1):
        tot_sum = num_shares * self.prices["a"].actual_value
        try:
            self.cash -= tot_sum
            self.shares["a"] += num_shares
            return available_cash - tot_sum, True
        except ValueError:
            return available_cash, False

    def sell(self, num_shares=1):
        revenue = num_shares * self.prices["a"].actual_value
        self.shares["a"] -= num_shares
        self.clean_zero_stock()
        return revenue


class Person:
    def __init__(self, portfolio: StockPortfolio = None, cash=1000, name="default"):
        self.portfolio = portfolio or StockPortfolio()
        self._cash = cash
        self.portfolio = defaultdict(int)
        self.name = name

    def buy(self, share, num_shares=1) -> bool:
        "If successfull returns True, else False"
        is_success = self.portfolio.buy(self.cash)
        return is_success

    def sell(self, share, num_shares=1):
        self.cash += self.portfolio.sell(num_shares)

    def get_full_value(self):
        return self.cash + self.portfolio.get_full_value()

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, num):
        if num < 0:
            raise ValueError(
                "Cash cannot be negative"
            )  # maybe add loans with interest later?
        self._cash = num
