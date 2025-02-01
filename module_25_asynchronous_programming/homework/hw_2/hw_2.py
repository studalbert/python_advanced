import asyncio
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool, cpu_count
from pathlib import Path

import aiohttp
import aiofiles
import requests

URL = "https://cataas.com/cat"
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / "cats"
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL, ssl=False) as response:
        # print(response.status)
        result = await response.read()
        await write_to_disk(result, idx)


async def write_to_disk(content: bytes, id: int):
    file_path = "{}/{}.png".format(OUT_PATH, id)
    async with aiofiles.open(file_path, mode="wb") as f:
        await f.write(content)


async def get_all_cats():

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)


def main():
    start = time.time()
    res = asyncio.run(get_all_cats())
    print(
        f"Время выполнения {CATS_WE_WANT} запросов с использованием корутин = {time.time() - start:.2f} секунд"
    )


def task(id):
    response = requests.get(URL)
    result = response.content
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode="wb") as f:
        f.write(result)


class RequestsOnWebsite:
    def responses_with_threadpool(self, count_req: int):
        start = time.time()
        with ThreadPool(processes=cpu_count() * 5) as pool:
            result = pool.map(task, range(1, count_req + 1))
        print(
            f"Время выполнения {count_req} запросов с использованием пула потоков = {time.time() - start:.2f} секунд"
        )

    def responses_with_processes(self, count_req: int):
        start = time.time()
        with Pool(processes=cpu_count()) as pool:
            result = pool.map(task, range(1, count_req + 1))
        print(
            f"Время выполнения {count_req} запросов с использованием пула процессов = {time.time() - start:.2f} секунд"
        )


if __name__ == "__main__":
    # 10 запросов
    # CATS_WE_WANT = 10
    # main()
    # req = RequestsOnWebsite()
    # req.responses_with_threadpool(10)
    # req.responses_with_processes(10)
    # 50 запросов
    CATS_WE_WANT = 50
    main()
    req = RequestsOnWebsite()
    req.responses_with_threadpool(50)
    req.responses_with_processes(50)
    # 100 запросов
    # CATS_WE_WANT = 100
    # main()
    # req = RequestsOnWebsite()
    # req.responses_with_threadpool(100)
    # req.responses_with_processes(100)
