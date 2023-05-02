import asyncio
import aiohttp

# true `parallel computing` means that an application runs multiple tasks at the
# same time where each task runs on a separate processing unit;
# `concurrency` means that an application is making progress on more than one
# task at the same time but may switch between these tasks instead of actually
# running them in parallel;
# `Global Interpreter Lock (GIL)` -> python code is single threaded even if you
# start multiple threads;

from random import randint
from time import perf_counter
from typing import Any, Awaitable, AsyncIterable
import requests


# A few handy JSON types
JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]


def http_get_sync(url: str) -> JSONObject:
    response = requests.get(url)
    return response.json()


async def http_get(url: str) -> JSONObject:
    return await asyncio.to_thread(http_get_sync, url)


async def http_get_aio(url: str) -> JSONObject:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


# The highest Pokemon id
MAX_POKEMON = 898


def get_random_pokemon_name_sync() -> str:
    pokemon_id = randint(1, MAX_POKEMON)
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    pokemon = http_get_sync(pokemon_url)
    return str(pokemon["name"])


async def get_random_pokemon_name() -> str:
    pokemon_id = randint(1, MAX_POKEMON)
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    pokemon = await http_get(pokemon_url)
    return str(pokemon["name"])


async def next_pokenmon(total: int) -> AsyncIterable[str]:
    for _ in range(total):
        name = await get_random_pokemon_name()
        yield name


async def main() -> None:
    # synchronous call
    time_before = perf_counter()
    for _ in range(20):
        get_random_pokemon_name_sync()
    print(f"Total time (synchronous): {perf_counter() - time_before}")

    # asynchronous call
    time_before = perf_counter()
    await asyncio.gather(*[get_random_pokemon_name() for _ in range(20)])
    print(f"Total time (asynchronous): {perf_counter() - time_before}")

    # retrieve the next 10 pokemon names
    async for name in next_pokenmon(10):
        print(name, end=" ")
    print()

    # asynchronous list comprehensions
    names = [name async for name in next_pokenmon(10)]
    print(names)


async def counter(until: int = 10) -> None:
    now = perf_counter()
    print("Started counter")
    for i in range(0, until):
        last = now
        await asyncio.sleep(0.01)
        now = perf_counter()
        print(f"{i}: Was asleep for {now - last}s")


def send_request(url: str) -> int:
    print("Sending HTTP request")
    response = requests.get(url)
    return response.status_code


async def send_async_request(url: str) -> int:
    return await asyncio.to_thread(send_request, url)


async def main_counter() -> None:

    status_code = send_request("https://www.google.com")
    print(f"Got HTTP response with status {status_code}")

    await counter()

    # correct way
    status_code, _ = await asyncio.gather(
        send_async_request("https://www.bing.com"), counter()
    )
    print(f"Got HTTP response with status {status_code}")

    # wrong way
    task = asyncio.create_task(counter())

    status_code = send_request("https://www.yandex.com")
    print(f"Got HTTP response with status {status_code}")

    await task


if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(main_counter())
