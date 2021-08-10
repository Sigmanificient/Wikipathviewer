from typing import List
from bs4.element import ResultSet, Tag


def filter_valid_links(links: ResultSet[Tag]) -> List[str]:
    filtered_links: List[str] = []

    for link in links:
        href: str = link.attrs.get('href')

        if is_valid(href):
            # Removing /wiki/
            filtered_links.append(href[6:])

    return filtered_links


def is_valid(link: str) -> bool:
    """Checks the link to be a wikipedia article."""
    if link is None:
        return False

    if ':' in link:
        return False

    if link.startswith('#'):
        return False

    return bool(link.startswith('/wiki/'))
