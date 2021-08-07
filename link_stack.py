seed_article = '/wiki/Python_(programming_language)'


class LinkStack:

    def __init__(self):
        # initializing with 1 link for process to work.
        self.__stack = [seed_article]

    def extend(self, link_list):
        if not link_list:
            return

        for link in link_list:
            if is_valid(link):
                self.__stack.append(link.href)

    def __next__(self):
        if not len(self.__stack):
            return

        return self.__stack.pop()


def is_valid(link):
    if link.href is None:
        return False

    href = link.href

    if link.href.startswith('#'):
        return False

    for optional_link in (
        'http://', 'https://',
        'en.wikipedia.org',
    ):
        if href.startswith(optional_link):
            href = href[len(optional_link):]

    return bool(href.startswith('/wiki/'))


link_stack = LinkStack()
