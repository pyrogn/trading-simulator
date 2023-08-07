import asyncio
from concurrent.futures import ThreadPoolExecutor
from aioconsole import ainput
from interface import CLIInterface
from concurrent.futures import CancelledError


cnt = 0


async def counter():
    global cnt
    while True:
        cnt += 1
        await asyncio.sleep(1)
        cli_interface.update_values("counter", cnt)
        if cnt > 10:
            break


async def some_coroutine():
    while True:
        line = await ainput()
        if line == "exit" or line == "e":  # how to make proper cancel?
            raise CancelledError
        cli_interface.update_values({"input_value": line, "last_command": line})


async def main():
    L = await asyncio.gather(some_coroutine(), counter())
    return L


cli_interface = CLIInterface("counter", "input_value", "last_command")
cli_interface.display()
try:
    res = asyncio.run(main())
    print(res)
except CancelledError:
    print("shut down")
