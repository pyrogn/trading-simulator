import os
from collections import defaultdict
from time import sleep
from functools import singledispatchmethod


class CLIInterface:
    def __init__(self, *keys):
        self.dict_values = defaultdict(str)
        for key in keys:
            self.dict_values[key] = ""

    @singledispatchmethod
    def update_values(self, arg):
        raise NotImplementedError

    @update_values.register
    def _(self, key: str, value: str):
        self.dict_values[key] = value
        self.display()

    @update_values.register
    def _(self, dict_update: dict):
        for key, value in dict_update.items():
            self.dict_values[key] = value
        self.display()

    def clear_screen(self):
        clear = "cls" if os.name == "nt" else "clear"
        os.system(clear)

    def display(self):
        max_len = len(max(self.dict_values, key=len))  # how to apply this dynamically?
        string_to_print = "\n".join(
            f"{key:<15} = {value}" for key, value in self.dict_values.items()
        )
        self.clear_screen()
        print(string_to_print)


if __name__ == "__main__":
    cli1 = CLIInterface("val1", "val23232")
    cli1.update_values("val1", "kv2")
    cli1.update_values("val23232", "kv232322")
    for i in range(10):
        num = str(i)
        if i % 2 == 0:
            cli1.update_values("val1", "kv" + num)
        elif i % 3 == 0:
            cli1.update_values({"val1": "kv_sim", "val23232": "kv_sim"})
        else:
            cli1.update_values("val23232", "kv" + num)
        sleep(0.5)
    cli1.display()
