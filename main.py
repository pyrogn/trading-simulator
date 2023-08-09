import asyncio
from datetime import datetime
from aioconsole import ainput
from interface import CLIInterface
from share_prices import SynthStockPrice, StockPrices
from concurrent.futures import CancelledError
from client_info import Person, StockPortfolio
from bot_logic import BotAction

REFRESH_RATE = 1  # update price of shares every N seconds
start_cash = 20000
length_of_game = 10000

stock1 = SynthStockPrice(length_of_game)
prices = StockPrices(stock1)
portfolio = StockPortfolio(prices)
person = Person(portfolio, start_cash)

bot_portfolio = StockPortfolio(prices)
bot = Person(bot_portfolio, cash=start_cash)
bot_action = BotAction(bot, bot_portfolio)

STOCK_NAME = "a"  # hardcode for now, but I don't think we need more than 2 stocks


async def global_tick():
    for current_price in prices:
        current_price = current_price[STOCK_NAME]
        if current_price is None:
            current_price = 999999  # patch. TODO: add format to messages

        bot_action.make_action()
        cli_interface.update_values(
            {
                "bot cash": bot.cash,  # f"{bot.cash:,.2f}",
                "bot portfolio": bot.portfolio.shares,  # dict(bot.portfolio.shares),
            }
        )

        cur_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        cur_total_balance = person.get_full_value()
        perc_tot_cash = cur_total_balance / start_cash
        bot_cur_total_balance = bot.get_full_value()
        bot_perc_tot_cash = bot_cur_total_balance / start_cash
        cli_interface.update_values(
            {
                "price": current_price,  # f"{current_price:,.2f}",
                "cur_time": cur_time,
                "cur tot bal": cur_total_balance,  # f"{cur_total_balance:,.2f} {perc_tot_cash:.2%}",
                "bot cur tot bal": bot_cur_total_balance,  # f"{bot_cur_total_balance:,.2f} {bot_perc_tot_cash:.2%}",
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
                "cash": person.cash,  # f"{person.cash:,.2f}",
                "bot cash": bot.cash,  # f"{bot.cash:,.2f}",
                # "available cash": f"{perc_available_cash:,.2%}",
                "portfolio": person.portfolio.shares,  # dict(person.portfolio.shares),
                "bot portfolio": bot.portfolio.shares,  # dict(bot.portfolio.shares),
                "last_command": line,
                "last_info": info_message,
            }
        )


async def main():
    L = await asyncio.gather(user_action(), global_tick())
    return L


cli_interface = CLIInterface(
    "price",
    "_1",
    "portfolio",
    "cash",
    "cur tot bal",
    "last_command",
    "last_info",  # to add color?
    "_2",
    "bot portfolio",
    "bot cash",
    "bot cur tot bal",
    "_3",
    "cur_time",
    colored_values={"price"},
    float_values={"cash", "bot cash", "price", "bot cur tot bal", "cur tot bal"},
    dict_format_values={"portfolio", "bot portfolio"},
)
cli_interface.display()
# init_cash_str = f"{person.cash:,}"
cli_interface.update_values(
    {
        "cash": person.cash,
        "bot cash": bot.cash,
        "cur tot bal": person.cash,
        "bot cur tot bal": bot.cash,
    }
)
try:
    res = asyncio.run(main())
    print(res)
except CancelledError:
    print("shut down")
    # print results and possibly leaderboard?
