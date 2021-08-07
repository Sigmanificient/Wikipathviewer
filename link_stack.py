seed_article = 'Python_(programming_language)'


class LinkStack:

    def __init__(self):
        # initializing with 1 link for process to work.
        self.__stack = [seed_article]

    def extend(self, link_list):
        if not link_list:
            return

        for link in link_list:
            href = link.attrs.get('href')

            if is_valid(href):
                # removing /wiki/
                self.__stack.append(href[6:])

    def __iter__(self):
        if not len(self.__stack):
            return

        yield self.__stack.pop()

    def __len__(self):
        return len(self.__stack)


def is_valid(link):
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


link_stack = LinkStack()
