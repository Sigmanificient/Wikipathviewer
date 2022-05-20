import re
from typing import List

WIKI_LINKS_PATTERN = re.compile(r'\/wiki\/([^":?#]+)')


def get_wiki_links(html_page: str) -> List[str]:
    """
    Return a list of links from the html page.
    """
    return re.findall(WIKI_LINKS_PATTERN, html_page)


def main():
    """
    Main function.
    """
    assert get_wiki_links('') == []

    assert get_wiki_links(
        '<html><body><a href="/wiki/Link">Link</a><a href="/wiki/Link2">Link2'
        '</a></body></html>'
    ) == ['Link', 'Link2']

    assert get_wiki_links(
        '<html><body><a href="/wiki/Link">Link</a><a href="Link2">Link2</a>'
        '<a href="/wiki/Link3">Link3</a></body></html>'
    ) == ['Link', 'Link3']


if __name__ == '__main__':
    main()
