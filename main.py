import curses
import requests
from bs4 import BeautifulSoup
from link_stack import link_stack

BASE_URL: str = 'https://en.wikipedia.org/wiki/'
std_screen = curses.initscr()


def update_status(c, link):
    total = c + len(link_stack)

    for y, line in enumerate(
        (
            f"last fetch: {link}",
            f"To fetch: {len(link_stack):,}",
            f"Total {c:,} / {total:,} ({(c / total) * 100:.2f})",
        )
    ):
        std_screen.addstr(y, 0, line)
    std_screen.refresh()


def main() -> None:
    """Main entry point for link fetching."""
    for c, link in enumerate(link_stack):
        response = requests.get(f"{BASE_URL}{link}")
        soup = BeautifulSoup(response.content, "html.parser")
        link_stack.extend(soup.findAll('a'))
        update_status(c, link)


if __name__ == '__main__':
    main()
