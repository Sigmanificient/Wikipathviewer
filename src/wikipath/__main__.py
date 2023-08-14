import asyncio

from .db import Database
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


async def process_request(resp, pool: FetchPool, db: Database):
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

    assert pool.last is not None
    await db.save_progress(
        pool.map.get_id(pool.last), pool.last, 
        [pool.map.get_id(art) for art in article_names]
    )


async def _async_main():
    db = await Database.connect()
    pool = FetchPool(SEED_ARTICLE)
    fetched = 0

    while not pool.empty:
        async with pool.fetch_next() as resp:
            await process_request(resp, pool, db)
            fetched += 1

        show_progress(fetched, pool.queued)

    await db.close()


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_async_main())


if __name__ == '__main__':
    main()