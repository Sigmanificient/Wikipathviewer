class LinkStack:

    def __init__(self):
        self.__stack = []

    def extend(self, link_list):
        if not link_list:
            return

        for link in link_list:
            if is_valid(link):
                self.__stack.append(link.href.remove_prefix('/wiki/'))

    def __next__(self):
        if not len(self.__stack):
            return

        return self.__stack.pop()


def is_valid(link):
    if link.href is None:
        return False

    if link.href.startswith('#'):
        return False

    if not link.href.startswith('/wiki/'):
        return False

    return True
