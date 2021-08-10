import curses
import requests
from bs4 import BeautifulSoup
from link_stack import link_stack
from filtering import filter_valid_links

BASE_URL: str = 'https://en.wikipedia.org/wiki/'
std_screen = curses.initscr()


def update_status(c, last_link):
    total = c + len(link_stack)
    std_screen.clear()

    for y, line in enumerate(
        (
            f"last fetch: {last_link}",
            f"To fetch: {len(link_stack):,}",
            f"Total {c:,} / {total:,} ({(c / total) * 100:.2f}%)",
        )
    ):
        std_screen.addstr(y, 0, line)
    std_screen.refresh()



def main() -> None:
    """Main entry point for link fetching."""
    for c, link in enumerate(link_stack):
        response = requests.get(f"{BASE_URL}{link}")
        soup = BeautifulSoup(response.content, "html.parser")

        links = filter_valid_links(soup.findAll('a'))
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
