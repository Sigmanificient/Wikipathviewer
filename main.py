import curses

import requests

from filtering import get_wiki_links
from link_stack import link_stack
from time import perf_counter

BASE_URL: str = 'https://en.wikipedia.org/wiki/'
std_screen = curses.initscr()
marker = perf_counter()


def update_status(c, last_link):
    total = c + len(link_stack)
    std_screen.clear()

    t = perf_counter() - marker

    for y, line in enumerate(
        (
            f"last fetch: {last_link}",
            f"To fetch: {len(link_stack):,}",
            f"Total {c:,} / {total:,} ({(c / total) * 100:.2f}%)",
            # Numbers of links fetched per second:
            f"{c / t:.2f}/s",
            f"{t:.2f}s",
        )
    ):
        std_screen.addstr(y, 0, line)
    std_screen.refresh()


def main() -> None:
    """Main entry point for link fetching."""
    for c, link in enumerate(link_stack):
        response = requests.get(f"{BASE_URL}{link}")

        links = get_wiki_links(response.text)
        link_stack.extend(links)

        with open("out/links.txt", "a+") as f:
            f.write(f'{link}\n')

        with open("out/links-relations", "a+") as f:
            indexes = ' '.join(
                map(str, (link_stack.index(link) for link in links))
            )

            f.write(f'{indexes}\n')

        update_status(c, link)


if __name__ == '__main__':
    main()
