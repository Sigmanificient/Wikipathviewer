from typing import List, Optional

from bs4.element import ResultSet, Tag

seed_article: str = 'Python_(programming_language)'


class LinkStack:

    def __init__(self):
        """initializing link stack with a seed article for fetching."""
        self.__stack: List[str] = [seed_article]

    def __iter__(self) -> Optional[str]:
        """Yields the next retrieved link while the stack is filled."""
        if not len(self.__stack):
            return

        yield self.__stack.pop()

    def __len__(self) -> int:
        """Return the number of links that still need to be fetched."""
        return len(self.__stack)

    def extend(self, link_list: ResultSet[Tag]) -> None:
        """Adds every valid wikipedia link to the stack."""
        if not link_list:
            return

        for link in link_list:
            href: str = link.attrs.get('href')

            if is_valid(href):
                # removing /wiki/
                self.__stack.append(href[6:])


def is_valid(link: str) -> bool:
    """Checks the link to be a wikipedia article."""
    if link is None:
        return False

    if link.startswith('#'):
        return False

    for optional_link in (
        'http://', 'https://',
        'en.wikipedia.org',
    ):
        if link.startswith(optional_link):
            link = link[len(optional_link):]

    return bool(link.startswith('/wiki/'))


link_stack: LinkStack = LinkStack()
