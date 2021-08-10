from typing import List, Optional

seed_article: str = 'Python_(programming_language)'


class LinkStack:

    def __init__(self):
        """initializing link stack with a seed article for fetching."""
        self.__stack: List[str] = [seed_article]

    def __iter__(self):
        """Initializing looping process."""
        return self

    def __next__(self) -> Optional[str]:
        """Yields the next retrieved link while the stack is filled."""
        if not len(self.__stack):
            return

        return self.__stack.pop()

    def __len__(self) -> int:
        """Return the number of links that still need to be fetched."""
        return len(self.__stack)

    def empty(self):
        """Return True if the stack is empty."""
        return not len(self)

    def extend(self, link_list: List[str]) -> None:
        """Adds every valid wikipedia link to the stack."""
        for link in link_list:
            if link not in self.__stack:
                self.__stack.append(link)

    def index(self, item):
        return self.__stack.index(item)


link_stack: LinkStack = LinkStack()
