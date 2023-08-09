import os
from collections import defaultdict
from time import sleep
import re
from functools import singledispatchmethod
from colorama import Fore, Style


def escape_ansi(line):
    "escape string with ANSI codes for color"
    line = str(line).replace(",", "")
    ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", line)


class CLIInterface:
    def __init__(
        self,
        *keys,
        colored_values: set = None,
        float_values: set = None,
        percent_values: set = None,
        dict_format_values: set = None,
    ):
        self.dict_values = defaultdict(str)
        self.prev_dict_values = defaultdict(str)
        for key in keys:
            self.dict_values[key] = ""
        self.colored_values = colored_values or {}
        self.float_values = float_values or {}
        self.percent_values = percent_values or {}
        self.dict_format_values = dict_format_values or {}

    def format_color(self, key, value):
        if key in self.colored_values:

            def str_to_float(string):
                try:
                    value = round(float(escape_ansi(string)), 2)
                except ValueError:
                    value = 0
                return value

            old_value, new_value = [
                str_to_float(i) for i in (self.prev_dict_values[key], value)
            ]
            if (
                old_value <= new_value
            ):  # TODO: if value is the same: return same formatting to get rid of flickering
                color = Fore.GREEN
            elif old_value > new_value:
                color = Fore.RED
            else:
                color = ""
            value = color + str(new_value) + Style.RESET_ALL
        return value

    def format_float(self, key, value):
        if key in self.float_values:
            value = f"{value:,.2f}"
        return value

    def format_percent(self, key, value):
        if key in self.percent_values:
            value = f"{value:,.2%}"
        return value

    def format_dict(self, key, value):
        if key in self.dict_format_values:
            value = dict(value)
        return value

    def add_formatting(self, key, value):
        value = self.format_float(key, value)
        value = self.format_percent(key, value)
        value = self.format_dict(key, value)
        value = self.format_color(key, value)  # if true then str type guaranteed
        return value

    @singledispatchmethod
    def update_values(self, arg):
        raise NotImplementedError

    @update_values.register
    def _(self, key: str, value: str):
        "update of a single value"
        self.dict_values[key] = value
        self.display()

    @update_values.register
    def _(self, dict_update: dict):
        "batch update values"
        for key, value in dict_update.items():
            self.dict_values[key] = value
        self.display()

    def clear_screen(self):
        clear = "cls" if os.name == "nt" else "clear"
        os.system(clear)

    def display(self):
        max_len = len(max(self.dict_values, key=len))  # how to apply this dynamically?

        string_to_print = "\n".join(
            f"{key:<15} = {self.add_formatting(key, value)}" if value else ""
            for key, value in self.dict_values.items()
        )
        self.prev_dict_values.update(self.dict_values)
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
