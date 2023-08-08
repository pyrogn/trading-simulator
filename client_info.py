from collections import defaultdict


class Person:
    def __init__(self, cash=1000, name="default"):
        self._cash = cash
        self.portfolio = defaultdict(int)
        self.name = name

    def buy(self, share, cur_price, num_shares=1):
        tot_sum = num_shares * cur_price
        self.portfolio[share] += num_shares
        self.cash -= tot_sum

    def sell(self, share, cur_price, num_shares=1):
        tot_sum = num_shares * cur_price
        self.portfolio[share] -= num_shares
        self.cash += tot_sum

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, num):
        self._cash = num

    @property
    def portfolio(self):
        return self._portfolio

    @portfolio.setter
    def portfolio(self, new_value):
        self._portfolio = new_value


class SharesPortfolio:
    def __init__(self, shares=None) -> None:
        self.shares = shares or []

    def get_total_price(self, share_prices) -> float:
        pass

    def update_portfolio(self):
        pass
