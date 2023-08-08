import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod

# from typing import Iterable, Iterator
from collections.abc import Iterator, Iterable


class SharePrices(Iterable):
    def __init__(self, n):
        pass

    def get_actual_price(share="a"):
        pass

    # @abstractmethod
    # def get_share_prices():
    #     raise NotImplementedError


class SynthSharePrices(SharePrices):
    def __init__(self, n):
        self.n = n
        self.init_value = np.random.randint(200, 1000)
        self.new_vals = np.random.default_rng().normal(0, 100, self.n)

    def get_actual_price(share="a"):
        return super().get_actual_price()

    def __iter__(self) -> tuple[float, str]:
        for new_val in self.new_vals:
            self.init_value += new_val
            yield self.init_value, datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


class RealSharePrices(SharePrices):
    "download real data from somewhere. Kaggle + random date? or real time?"
    pass


if __name__ == "__main__":
    g1 = SynthSharePrices(5)
    for i in g1:
        print(i)
