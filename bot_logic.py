from client_info import StockPortfolio, Person
from collections import deque
from itertools import islice


class BotAction:
    def __init__(self, person: Person, portfolio: StockPortfolio):
        self.person = person
        self.portfolio = portfolio
        self.cash = lambda: self.person.cash
        self.current_prices = lambda: self.portfolio.prices.get_actual_price()["a"]
        self.history_prices = deque([0])
        self.history_prices_changes = deque()

    def make_action(self):
        self.log_prices()
        self.strategy_mean()

    def strategy_diff(self):
        "not used because it is stupid"
        if all(
            i == "-" for i in list(self.history_prices_changes)[-2:]
        ):  # TODO: make it more performant and smarter
            self.person.buy("a")

        if all(i == "+" for i in list(self.history_prices_changes)[-2:]):
            self.person.sell("a")

    def strategy_mean(self):
        slicing_mean = sum(
            islice(self.history_prices, 0, len(self.history_prices) - 1)
        ) / len(self.history_prices)
        if len(self.history_prices) >= 5:
            if self.history_prices[len(self.history_prices) - 1] <= slicing_mean:
                self.person.buy("a")
            else:
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
