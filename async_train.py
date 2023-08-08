import asyncio
from aioconsole import ainput
from interface import CLIInterface
from share_prices import SynthSharePrices
from concurrent.futures import CancelledError
from client_info import Person, SharesPortfolio


start_cash = 1000
prices = SynthSharePrices(100)
portfolio = Person(start_cash)
current_price = None


async def counter():
    global current_price
    for current_price, cur_time in prices:
        await asyncio.sleep(1)
        cur_total_balance = portfolio.cash + portfolio.portfolio["a"] * current_price
        perc_tot_cash = cur_total_balance / start_cash
        cli_interface.update_values(
            {
                "price": f"{current_price:,.2f}",
                "cur_time": cur_time,
                "cur tot bal": f"{cur_total_balance:,.2f} {perc_tot_cash:.2%}",
            }
        )
    raise CancelledError


async def some_coroutine():
    while True:
        line = await ainput()
        if line == "exit" or line == "e":  # how to make proper cancel?
            raise CancelledError
        elif line == "b":
            portfolio.buy("a", current_price)
        elif line == "s":
            portfolio.sell("a", current_price)

        cli_interface.update_values(
            {
                "cash": f"{portfolio.cash:,.2f}",
                # "available cash": f"{perc_available_cash:,.2%}",
                "portfolio": dict(portfolio.portfolio),
                "last_command": line,
            }
        )


async def main():
    L = await asyncio.gather(some_coroutine(), counter())
    return L


cli_interface = CLIInterface(
    "price",
    "cur_time",
    "",
    "portfolio",
    "cash",
    # "available cash",
    "cur tot bal",
    "last_command",
)
cli_interface.display()
init_cash_str = f"{portfolio.cash:,}"
cli_interface.update_values(
    {
        "cash": init_cash_str,
        # "available cash": init_cash_str,
        "cur tot bal": init_cash_str,
    }
)
try:
    res = asyncio.run(main())
    print(res)
except CancelledError:
    print("shut down")
