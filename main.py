import requests
from bs4 import BeautifulSoup
from link_stack import link_stack

BASE_URL: str = 'https://en.wikipedia.org/wiki/'


def main() -> None:
    """Main entry point for link fetching."""
    for link in link_stack:
        response = requests.get(f"{BASE_URL}{link}")
        soup = BeautifulSoup(response.content, "html.parser")
        link_stack.extend(soup.findAll('a'))
        print(len(link_stack))


if __name__ == '__main__':
    main()
