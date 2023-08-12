from client_info import StockPortfolio, Person
from collections import deque
from itertools import islice
from logger import setup_logger

logger = setup_logger("bot_actions", "bot_actions.log")


class BotAction:
    "Get bot action (buy, sell, wait) from stock prices"

    def __init__(self, person: Person, portfolio: StockPortfolio, STOCK_NAME="a"):
        self.person = person
        self.portfolio = portfolio

        self.current_prices = lambda: self.portfolio.prices.get_actual_price()["a"]
        self.history_prices = deque()
        self.history_prices_changes = deque()
        self.STOCK_NAME = STOCK_NAME  # bot actions on this stock only

    def make_action(self):
        self.log_prices()
        self.strategy_mean()
        # self.strategy_diff()

    def strategy_diff(self):
        "not used because it is stupid"
        if all(
            i == "-" for i in list(self.history_prices_changes)[-2:]
        ):  # TODO: make it more performant and smarter
            self.person.buy(self.STOCK_NAME)

        if all(i == "+" for i in list(self.history_prices_changes)[-2:]):
            self.person.sell(self.STOCK_NAME)

    def strategy_mean(self):
        slice_for_mean = list(
            islice(self.history_prices, 0, len(self.history_prices) - 1)
        )
        len_of_slice = len(slice_for_mean)
        if len_of_slice > 0:
            slicing_mean = sum(slice_for_mean) / len_of_slice
            logger.info(f"slice of prices: {slice_for_mean}")
            logger.info(f"slicing mean: {slicing_mean}")
            if len(self.history_prices) >= 5:
                if self.history_prices[len(self.history_prices) - 1] <= slicing_mean:
                    action = "buy"
                    self.person.buy(self.STOCK_NAME)
                else:
                    action = "sell"
                    self.person.sell(self.STOCK_NAME)
                logger.info(f"action: {action}")

    def log_prices(self):
        cur_prices = self.current_prices()
        self.history_prices.append(cur_prices)
        if len(self.history_prices) >= 2:
            if self.history_prices[-2] <= cur_prices:
                self.history_prices_changes.append("+")
            else:
                self.history_prices_changes.append("-")

            if len(self.history_prices) > 10:  # keep memory requirements constant
                _ = self.history_prices.popleft()
            if len(self.history_prices_changes) > 10:
                _ = self.history_prices_changes.popleft()

        logger.info(f"prices: {self.history_prices}")
