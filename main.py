import requests
from bs4 import BeautifulSoup
from link_stack import link_stack

BASE_URL = 'https://en.wikipedia.org'


def main():
    for link in link_stack:
        response = requests.get(f"{BASE_URL}{link}")
        soup = BeautifulSoup(response.content, "html.parser")
        link_stack.extend(soup.findAll('a'))
        print(len(link_stack))


if __name__ == '__main__':
    main()