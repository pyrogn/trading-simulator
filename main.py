import asyncio
from datetime import datetime
from aioconsole import ainput
from interface import CLIInterface
from share_prices import SynthStockPrice, StockPrices
from concurrent.futures import CancelledError
from client_info import Person, StockPortfolio

REFRESH_RATE = 1  # update price of shares every N seconds
start_cash = 1000
length_of_game = 100

stock1 = SynthStockPrice(length_of_game)
prices = StockPrices(stock1)
portfolio = StockPortfolio(prices)
person = Person(portfolio, start_cash)

STOCK_NAME = "a"  # hardcode for now, but I don't think we need more than 2 stocks


async def global_tick():
    for current_price in prices:
        current_price = current_price[STOCK_NAME]
        if current_price is None:
            current_price = 999999  # patch. TODO: add format to messages

        cur_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        cur_total_balance = person.get_full_value()
        perc_tot_cash = cur_total_balance / start_cash
        cli_interface.update_values(
            {
                "price": f"{current_price:,.2f}",
                "cur_time": cur_time,
                "cur tot bal": f"{cur_total_balance:,.2f} {perc_tot_cash:.2%}",
            }
        )
        await asyncio.sleep(REFRESH_RATE)
    raise CancelledError


async def user_action():
    while True:
        line = await ainput()
        info_message = ""
        if line in {"exit", "e", "q", "quit"}:
            raise CancelledError  # how to make proper cancel?
        elif line == "b":
            status = person.buy(STOCK_NAME)
            info_message = "SUCCESS BUY" if status else "FAIL BUY. NOT ENOUGH MONEY"
        elif line == "s":
            status = person.sell(STOCK_NAME)
            info_message = "SUCCESS SELL" if status else "FAIL SELL. NOT ENOUGH SHARES"
        else:
            info_message = "UNKNOWN COMMAND"

        cli_interface.update_values(
            {
                "cash": f"{person.cash:,.2f}",
                # "available cash": f"{perc_available_cash:,.2%}",
                "portfolio": dict(person.portfolio.shares),
                "last_command": line,
                "last_info": info_message,
            }
        )


async def main():
    L = await asyncio.gather(user_action(), global_tick())
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
    "last_info",
    colored_values={"price"},
)
cli_interface.display()
init_cash_str = f"{person.cash:,}"
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
