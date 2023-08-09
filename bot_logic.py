from client_info import StockPortfolio, Person
from share_prices import StockPrices
from collections import deque


class BotAction:
    def __init__(self, person: Person, portfolio: StockPortfolio, prices: StockPrices):
        self.person = person
        self.portfolio = portfolio
        self.prices = prices
        self.cash = lambda: self.person.cash
        self.current_prices = lambda: self.prices.get_actual_price()["a"]
        self.history_prices = deque([0])
        self.history_prices_changes = deque()

    def make_action(self):
        self.log_prices()
        if all(
            i == "-" for i in list(self.history_prices_changes)[-2:]
        ):  # TODO: make it more performant and more smart
            self.person.buy("a")

        if all(i == "+" for i in list(self.history_prices_changes)[-2:]):
            self.person.sell("a")

    def log_prices(self):
        cur_prices = self.current_prices()
        self.history_prices.append(cur_prices)

        if self.history_prices[-2] <= cur_prices:
            self.history_prices_changes.append("+")
        else:
            self.history_prices_changes.append("-")

        if len(self.history_prices) > 10:  # keep memory requirements constant
            _ = self.history_prices.popleft()
        if len(self.history_prices_changes) > 10:  # keep memory requirements constant
            _ = self.history_prices_changes.popleft()
