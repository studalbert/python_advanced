import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup


URL = "https://www.geeksforgeeks.org/"
all_links = set()


async def crawler(link, deep=3):
    deep -= 1
    if deep == 0:
        return
    links = set()

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        async with client.get(URL) as response:
            result = await response.read()
            soup = BeautifulSoup(result, "html.parser")

            for link in soup.find_all("a", href=True):

                if link.get("href").startswith(
                    "http"
                ) and "geeksforgeeks.org" not in link.get("href"):
                    print(link.get("href"))
                    links.add(link.get("href"))

            new_links = links - all_links
            all_links.update(new_links)

            await asyncio.gather(*(write_to_disk(link) for link in new_links))
    await asyncio.gather(*(crawler(link, deep=deep) for link in new_links))


async def write_to_disk(link):
    async with aiofiles.open("links.txt", mode="a") as f:
        await f.write(link + "\n")


def main():
    res = asyncio.run(crawler(URL, 4))


if __name__ == "__main__":
    main()
