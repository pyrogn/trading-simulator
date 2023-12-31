from client_info import StockPortfolio, Person
from collections import deque
from itertools import islice
from logger import setup_logger
import random

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
        self._initial_value = self.person.get_full_value()

    def make_action(self):
        self.log_prices()
        self.strategy_mean()
        self.strategy_do_not_lose()
        # self.strategy_diff()
        logger.info(
            f"cur value: {self.person.get_full_value()}, shares: {dict(self.portfolio.shares)}"
        )

    def strategy_do_not_lose(self):
        cur_value = self.person.get_full_value()
        prop_decline = (cur_value - self._initial_value) / self._initial_value

        if prop_decline <= 0:
            if abs(int(prop_decline * 100)) >= random.randint(1, 8):
                logger.info(
                    f"sell all. Cur value: {cur_value}, Initial value: {self._initial_value}"
                )
                self.person.sell_all()
                self._initial_value = self.person.get_full_value()

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
                if (
                    self.history_prices[len(self.history_prices) - 1]
                    <= slicing_mean + 100
                ):
                    action = "buy"
                    self.person.buy(self.STOCK_NAME)
                elif (
                    self.history_prices[len(self.history_prices) - 1]
                    >= slicing_mean - 100
                ):
                    action = "sell"
                    self.person.sell(self.STOCK_NAME)
                else:
                    action = "wait"
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
