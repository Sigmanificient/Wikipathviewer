from collections import defaultdict
from typing import List, Optional, Dict, Set

seed_article: str = 'Python_(programming_language)'


class LinkStack:

    def __init__(self):
        """initializing link stack with a seed article for fetching."""
        self.__stack: Dict[str, int] = defaultdict(int)
        self.__stack[seed_article] = 1
        self.__counter = 2

        self.__remaining: Set[str] = {seed_article}
        self.__left = 0  # hack to make the first fetching work

    def __iter__(self):
        """Initializing looping process."""
        return self

    def __next__(self) -> Optional[str]:
        """Yields the next retrieved link while the stack is filled."""
        self.__left -= 1
        return self.__remaining.pop()

    def __len__(self) -> int:
        """Return the number of links that still need to be fetched."""
        return self.__counter - self.__left

    def empty(self):
        """Return True if the stack is empty."""
        return not self.__left

    def extend(self, link_list: List[str]) -> None:
        """Adds every valid wikipedia link to the stack."""
        for link in link_list:
            if self.__stack[link] == 0:
                self.__stack[link] = self.__counter
                self.__remaining.add(link)

                self.__counter += 1
                self.__left += 1

    def index(self, item):
        return self.__stack[item]


link_stack: LinkStack = LinkStack()
