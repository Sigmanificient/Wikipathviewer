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


def main() -> None:
    pool = FetchPool(SEED_ARTICLE)
    fetched = 0

    while not pool.empty:
        response = pool.fetch_next()
        if not response.ok:
            continue

        fetched += 1
        links = parse_links(response.text)
        if links is None:
            continue

        article_names = clean_up_names(links)
        pool.extend(article_names)

        show_progress(fetched, pool.queued)
        # save_progess(article_names)


if __name__ == '__main__':
    main()