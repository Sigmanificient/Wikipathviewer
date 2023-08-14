import asyncio
import time

from .fetch_pool import FetchPool
from .utils import clean_up_names, parse_links

SEED_ARTICLE: str = "Python_(programming_language)"


def show_progress(fetched, queued):
    total = fetched + queued
    percent = (fetched / (total)) * 100
    print(
        f"Progress: {fetched:,}/{total:,}"
        f" - {percent:.2f}% - {queued:,} Remaining "
   )


async def process_request(resp, pool):
    if resp.status != 200:
        return

    article_text = await resp.text()

    links = parse_links(article_text)
    if links is None:
        print("! No links found")
        return
 
    print("Possible new links:", ll := len(links))
    article_names = clean_up_names(links)
    print("Filtered out:", ll - len(article_names))
    pool.extend(article_names)


async def _async_main():
    pool = FetchPool(SEED_ARTICLE)
    fetched = 0

    while not pool.empty:
        async with pool.fetch_next() as resp:
            await process_request(resp, pool)
            fetched += 1

        show_progress(fetched, pool.queued)
        time.sleep(.2)
        # save_progess(article_names)


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_async_main())


if __name__ == '__main__':
    main()