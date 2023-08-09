import os
from collections import defaultdict
from time import sleep
import re
from functools import singledispatchmethod
from colorama import Fore, Style


def escape_ansi(line):
    ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", line)


class CLIInterface:
    def __init__(self, *keys, colored_values: set = None):
        self.dict_values = defaultdict(str)
        for key in keys:
            self.dict_values[key] = ""
        self.colored_values = colored_values or {}

    def update_color(self, key, value):
        if key in self.colored_values:

            def str_to_float(string):
                try:
                    value = float(
                        escape_ansi(string).replace(",", "")
                    )  # TODO: i want here preformatted value
                except ValueError:
                    value = 0
                return value

            old_value, new_value = [
                str_to_float(i) for i in (self.dict_values[key], value)
            ]
            if old_value < new_value:
                color = Fore.GREEN
            elif old_value > new_value:
                color = Fore.RED
            else:
                color = ""
            value = color + str(new_value) + Style.RESET_ALL
        return value

    @singledispatchmethod
    def update_values(self, arg):
        raise NotImplementedError

    @update_values.register
    def _(self, key: str, value: str):
        value = self.update_color(key, value)
        self.dict_values[key] = value
        self.display()

    @update_values.register
    def _(self, dict_update: dict):
        for key, value in dict_update.items():
            value = self.update_color(key, value)
            self.dict_values[key] = value
        self.display()

    def clear_screen(self):
        clear = "cls" if os.name == "nt" else "clear"
        os.system(clear)

    def display(self):
        max_len = len(max(self.dict_values, key=len))  # how to apply this dynamically?
        string_to_print = "\n".join(
            f"{key:<15} = {value}" if value else ""
            for key, value in self.dict_values.items()
        )
        self.clear_screen()
        print(string_to_print)


if __name__ == "__main__":
    from itertools import chain

    cli1 = CLIInterface("val1", "val23232", colored_values={"val1"})
    # cli1.update_values("val1", "kv2")
    # cli1.update_values("val23232", "kv232322")
    for i in chain(range(5), range(5, 0, -1)):
        num = str(i)
        if i % 2 == 0:
            cli1.update_values("val1", num)
        elif i % 3 == 0:
            cli1.update_values({"val1": num, "val23232": "kv_sim"})
        else:
            cli1.update_values("val23232", "kv" + num)
        sleep(0.3)
    cli1.display()
