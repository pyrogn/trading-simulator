from collections import defaultdict
from share_prices import StockPrice, StockPrices


class StockPortfolio:
    def __init__(self, prices: StockPrices):
        self.shares = defaultdict(int)
        self.prices = prices

    def get_full_value(self) -> float:
        return sum(
            self.prices.get_actual_price() * self.shares["a"]
            for i in self.shares  # fix for multiple shares
        )

    def update_portfolio(self):
        pass

    def clean_zero_stock(self):
        keys_to_delete = []
        for key in self.shares:
            if self.shares[key] <= 0:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del self.shares[key]

    def buy(self, available_cash, num_shares=1) -> tuple[float, bool]:
        tot_sum = num_shares * self.prices.get_actual_price()  # add name of share
        try:
            left_cash = available_cash - tot_sum

            if left_cash < 0:
                raise ValueError
            self.shares["a"] += num_shares
            return left_cash, True
        except ValueError:
            return available_cash, False

    def sell(self, num_shares=1):
        # ensure to sell only if you have one
        revenue = num_shares * self.prices.get_actual_price()
        if self.shares["a"] > 0:
            self.shares["a"] -= num_shares
            self.clean_zero_stock()
            return revenue, True
        self.clean_zero_stock()
        return 0, False


class Person:
    def __init__(self, portfolio: StockPortfolio = None, cash=1000, name="default"):
        self.portfolio = portfolio or StockPortfolio()
        self._cash = cash
        self.name = name

    def buy(self, share, num_shares=1) -> bool:
        "If successfull returns True, else False"
        self.cash, is_success = self.portfolio.buy(self.cash, num_shares)
        return is_success

    def sell(self, share, num_shares=1):
        revenue, is_success = self.portfolio.sell(num_shares)
        self.cash += revenue
        return is_success

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
