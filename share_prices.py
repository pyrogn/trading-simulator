from typing import Any, Iterator
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod
from functools import singledispatchmethod

# from typing import Iterable, Iterator
from collections.abc import Iterator, Iterable


class StockPrice(Iterable):
    def __init__(self, n, name):
        pass

    def get_actual_price(share):
        pass

    # @abstractmethod
    # def get_share_prices():
    #     raise NotImplementedError


class SynthStockPrice(StockPrice):
    def __init__(self, n, name="a"):
        self.n = n
        self.name = name
        self.actual_value = None

        self.generate_values()

    def generate_values(self):
        self.actual_value = np.random.randint(200, 1000)
        self.new_vals = np.random.default_rng().normal(0, 100, self.n)

    def __iter__(self) -> tuple[str, float]:
        for new_val in self.new_vals:
            self.actual_value += new_val
            if self.actual_value < 0:
                self.actual_value = 50  # TODO: change hardcode
                yield self.name, self.actual_value
            else:
                yield self.name, self.actual_value


class RealStockPrice(StockPrice):
    """data is from https://www.kaggle.com/datasets/paultimothymooney/stock-market-data
    It has daily data but it gets normalized and iterated with a very short delay so this game is still fun
    """

    #
    pass


class StockPrices:
    """union of all stock prices. it adds timestamp
    It is composition of individual prices
    Think about programmatic way to capture all generated stocks"""

    def __init__(self, *stock_price):
        self.stock_price = stock_price

    def __iter__(self):
        for prices in zip(*self.stock_price):
            yield {name: price for name, price in prices}

    def get_actual_price(self):
        return {stock.name: stock.actual_value for stock in self.stock_price}

    # def __getattribute__(self, __name: str = "a") -> Any:
    #     return self.stock_price
    # for prices in zip(self.stock_price):  # what if they're unequal?
    #     # breakpoint()
    #     yield {price.name: next(price) for price in prices}
    # yield {prices.name: price for prices in self.stock_price for price in prices}


if __name__ == "__main__":
    s1 = SynthStockPrice(15, "a")
    s2 = SynthStockPrice(15, "b")
    # print(list(iter(s1)))
    stock_prices = StockPrices(s1, s2)
    print(len(list(iter(stock_prices))))
    for i in stock_prices:
        print(i)
