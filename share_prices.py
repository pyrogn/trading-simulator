import numpy as np
import pandas as pd
from pathlib import Path
import random
from statistics import NormalDist
from collections.abc import Iterable
from logger import setup_logger

TARGET_MEAN = 2000
logger = setup_logger("prices", "prices.log")


class StockPrice(Iterable):
    def __init__(self, n, name):
        pass


class SynthStockPrice(StockPrice):
    def __init__(self, n, name="a"):
        self.n = n
        self.name = name
        self.actual_value = None

        self.generate_values()

    def generate_values(self):
        self.actual_value = np.random.randint(TARGET_MEAN - 300, TARGET_MEAN + 300)
        self.new_vals = np.random.default_rng().normal(0, 100, self.n)

    def __iter__(self) -> tuple[str, float]:
        for new_val in self.new_vals:
            self.actual_value += new_val
            z = (self.actual_value - TARGET_MEAN) / 1000
            if (
                NormalDist().cdf(abs(z)) - 0.5 > random.randint(1, 100) / 100
            ):  # if score further from target mean, then correct it with random factors
                self.actual_value -= z * random.randint(1, 100)

            if self.actual_value < 50:
                self.actual_value = np.random.randint(100, 150)  # TODO: change hardcode
                yield self.name, self.actual_value
            else:
                yield self.name, self.actual_value


class RealStockPrice(StockPrice):
    """data is from https://www.kaggle.com/datasets/paultimothymooney/stock-market-data
    It has daily data but it gets normalized and iterated with a very short delay so this game is still fun
    """

    def __init__(self, n, name):
        names = ["AAPL", "AMZN", "NFLX"]
        self.name = random.choice(names)
        d = pd.read_csv(Path("data") / f"{self.name}.csv", sep=",", usecols=["Close"])
        listd = np.array(d["Close"])
        self.xc = (listd - listd.mean()) / listd.std() * 1000 + 1000
        self.actual_value = self.xc[0]
        self.name = "a"  # delete it

    def __iter__(self) -> tuple[str, float]:
        for self.actual_value in self.xc:
            if self.actual_value < 0:
                self.actual_value = 50  # TODO: change hardcode
                yield self.name, self.actual_value  # change to self.name
            else:
                yield self.name, self.actual_value


class StockPrices:
    """Union of all stock prices
    It is composition of individual prices
    Maybe to think about programmatic way to capture all generated stocks"""

    def __init__(self, *stock_price):
        self.stock_price = stock_price

    def __iter__(self):
        for prices in zip(*self.stock_price):
            yield {name: price for name, price in prices}

    def get_actual_price(self):
        prices = {stock.name: stock.actual_value for stock in self.stock_price}
        logger.info(prices)
        return prices


if __name__ == "__main__":
    s1 = SynthStockPrice(15, "a")
    s2 = SynthStockPrice(15, "b")
    # print(list(iter(s1)))
    stock_prices = StockPrices(s1, s2)
    print(len(list(iter(stock_prices))))
    for i in stock_prices:
        print(i)
