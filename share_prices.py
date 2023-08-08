from typing import Iterator
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
        self.init_value = np.random.randint(200, 1000)
        self.new_vals = np.random.default_rng().normal(0, 100, self.n)
        self.new_vals = self.new_vals[self.new_vals < 0] = 0

    def __iter__(self) -> tuple[float, str]:
        for new_val in self.new_vals:
            self.init_value += new_val
            self.actual_value = self.init_value  # to use it outside of iteration
            yield self.init_value


class RealStockPrice(StockPrice):
    """data is from https://www.kaggle.com/datasets/paultimothymooney/stock-market-data
    It has daily data but it gets normalized and iterated with a very short delay so this game is still fun
    """

    #
    pass


class StockPrices(StockPrice):
    """union of all stock prices. it adds timestamp
    It is composition of individual prices
    Think about programmatic way to capture all generated stocks"""

    def __init__(self, *stock_price):
        self.stock_price = stock_price

    def __iter__(self) -> Iterator[dict[str, float], str]:
        "iter by all iterators"

        yield {price.name: price.actual_price for price in self.stock_price}


if __name__ == "__main__":
    g1 = SynthStockPrice(5)
    for i in g1:
        print(i)
