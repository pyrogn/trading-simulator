# async def ainput(prompt: str = "") -> str:
#     with ThreadPoolExecutor(1, "AsyncInput") as executor:
#         return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)


# async def ainput(prompt: str = ""):
#     with ThreadPoolExecutor(1, "ainput") as executor:
#         return (
#             await asyncio.get_event_loop().run_in_executor(executor, input, prompt)
#         ).rstrip()
