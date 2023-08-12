from collections import defaultdict
from share_prices import StockPrices


class StockPortfolio:
    "Portfolio with stocks which should have every Person"

    def __init__(self, prices: StockPrices):
        self.shares = defaultdict(int)
        self.prices = prices

    def get_full_value(self) -> float:
        return sum(
            self.prices.get_actual_price()[i] * self.shares[i] for i in self.shares
        )

    def sell_all(self, share: str) -> float:
        is_success = True
        total_revenue = 0
        while is_success:
            revenue, is_success = self.sell(share, num_shares=1)
            total_revenue += revenue
        return total_revenue

    def buy_all(self, available_cash: float, share: str) -> float:
        is_success = True
        while is_success:
            available_cash, is_success = self.buy(available_cash, share, num_shares=1)
        return available_cash

    def clean_zero_stock(self):
        keys_to_delete = []
        for key in self.shares:
            if self.shares[key] <= 0:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del self.shares[key]

    def buy(
        self, available_cash: float, share: str, num_shares=1
    ) -> tuple[float, bool]:
        tot_sum = num_shares * self.prices.get_actual_price()[share]
        try:
            left_cash = available_cash - tot_sum

            if left_cash < 0:
                raise ValueError
            self.shares[share] += num_shares
            return left_cash, True
        except ValueError:
            return available_cash, False

    def sell(self, share: str, num_shares=1) -> tuple[float, bool]:
        revenue = num_shares * self.prices.get_actual_price()[share]
        if self.shares[share] > 0:
            self.shares[share] -= num_shares
            self.clean_zero_stock()
            return revenue, True
        self.clean_zero_stock()
        return 0, False


class Person:
    "Main agent that make actions"

    def __init__(self, portfolio: StockPortfolio, cash=1000):
        self.portfolio = portfolio
        self._cash = cash

    def buy(self, share="a", num_shares=1) -> bool:
        """
        Tries to buy a share
        If successfull returns True, else False
        """
        self.cash, is_success = self.portfolio.buy(self.cash, share, num_shares)
        return is_success

    def sell(self, share="a", num_shares=1):
        "Tries to sell a share"
        revenue, is_success = self.portfolio.sell(share, num_shares)
        self.cash += revenue
        return is_success

    def sell_all(self, share="a"):
        "Sell all shares. No checks on success operation"
        revenue = self.portfolio.sell_all(share)
        self.cash += revenue
        return bool(revenue)

    def buy_all(self, share="a"):
        "Buy shares on all available money"
        old_cash_amt = self.cash
        self.cash = self.portfolio.buy_all(self.cash, share)
        return self.cash != old_cash_amt

    def get_full_value(self):
        return self.cash + self.portfolio.get_full_value()

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, num):
        # it is better to add protection so only this class can overwrite cash amount
        if num < 0:
            raise ValueError(
                "Cash cannot be negative"
            )  # maybe add loans with interest later?
        self._cash = num
