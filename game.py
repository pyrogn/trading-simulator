import asyncio
from datetime import datetime
from aioconsole import ainput
from concurrent.futures import CancelledError

from interface import CLInterface
from share_prices import SynthStockPrice, StockPrices, RealStockPrice
from bot_logic import BotAction
from client_info import Person, StockPortfolio

REFRESH_RATE = 1  # update price of shares every N seconds
STOCK_NAME = "a"

start_cash = 8000
length_of_game = 10000

stock1 = SynthStockPrice(length_of_game)
# stock1 = RealStockPrice(length_of_game, "AAPL") # real prices aren't that interesting
prices = StockPrices(stock1)
portfolio = StockPortfolio(prices)
person = Person(portfolio, start_cash)

bot_portfolio = StockPortfolio(prices)
bot = Person(bot_portfolio, cash=start_cash)
bot_action = BotAction(bot, bot_portfolio)

get_current_time = lambda: datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


async def global_tick():
    for current_price in prices:
        current_price = current_price[STOCK_NAME]

        bot_action.make_action()

        cur_time = get_current_time()
        cur_total_balance = person.get_full_value()
        bot_cur_total_balance = bot.get_full_value()
        cli_interface.update_values(
            {
                "price": current_price,
                "cur_time": cur_time,
                "cur tot bal": cur_total_balance,
                "bot cur tot bal": bot_cur_total_balance,
                "bot cash": bot.cash,
                "bot portfolio": bot.portfolio.shares,
            }
        )
        await asyncio.sleep(REFRESH_RATE)
    raise CancelledError


def perform_command_on_input(line: str) -> str:
    command_action_message = {
        "b": (person.buy, "SUCCESS BUY", "FAIL BUY. NOT ENOUGH MONEY"),
        "ba": (person.buy_all, "SUCCESS BUY", "FAIL BUY. NOT ENOUGH MONEY"),
        "s": (person.sell, "SUCCESS SELL", "FAIL SELL. ZERO SHARES"),
        "sa": (
            person.sell_all,
            "SUCCESS ALL SELL",
            "FAIL SELL. ZERO SHARES",
        ),
    }
    try:
        select_action = command_action_message[line]
        status = select_action[0](STOCK_NAME)
        info_message = select_action[1] if status else select_action[2]
        return info_message
    except KeyError:
        return "UNKNOWN COMMAND"


async def user_action():
    while True:
        line = await ainput()
        info_message = ""
        if line in {"exit", "e", "q", "quit"}:
            raise CancelledError  # how to make proper cancel?
        info_message = perform_command_on_input(line)

        cli_interface.update_values(
            {
                "cash": person.cash,
                "portfolio": person.portfolio.shares,
                "last_command": line,
                "last_info": info_message,
            }
        )


async def main():
    L = await asyncio.gather(user_action(), global_tick())
    return L


cli_interface = CLInterface(
    "price",
    "_1",
    "portfolio",
    "cash",
    "cur tot bal",
    "last_command",
    "last_info",
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

cli_interface.update_values(
    {
        "cash": person.cash,
        "bot cash": bot.cash,
        "cur tot bal": person.cash,
        "bot cur tot bal": bot.cash,
    }
)
cli_interface.clear_screen()
print(
    "Keyboard commands:",
    "e/q - quit",
    "b - buy a share",
    "ba - buy shares on all available money",
    "s - sell a share",
    "sa - sell all shares",
    sep="\n",
)
_ = input("Press <Enter> to Start")

cli_interface.display()
try:
    res = asyncio.run(main())
    print(res)
except CancelledError:
    print("shut down")
    # print results and possibly leaderboard?
