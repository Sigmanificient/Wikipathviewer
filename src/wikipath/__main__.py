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


async def process_request(resp, article_id, pool: FetchPool, db: Database):
    article_name = pool.map.get_name(article_id)

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

    await db.save_progress(
        article_id, article_name, 
        [pool.map.get_id(art) for art in article_names]
    )


async def _async_main():
    db = await Database.connect()
    pool = FetchPool(SEED_ARTICLE)
    fetched = 0

    while not pool.empty:
        id_, res_coro = pool.fetch_next()

        async with res_coro as resp:
            await process_request(resp, id_, pool, db)
            fetched += 1

        show_progress(fetched, pool.queued)

    await db.close()


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(_async_main())


if __name__ == '__main__':
    main()