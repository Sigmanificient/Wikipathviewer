from queue import Queue
from urllib.parse import quote

from .indexed_map import IndexedMap

import aiohttp

BASE_URL: str = 'https://en.wikipedia.org/wiki'


class FetchPool:

    def __init__(self, seed):
        self._idxm: IndexedMap[str] = IndexedMap()
        idx = self._idxm.add(seed)

        self._queue = Queue()
        self._queue.put(idx)

        self._session = aiohttp.ClientSession()

    @property
    def queued(self) -> int:
        return self._queue.qsize()

    @property
    def empty(self) -> int:
        return not self.queued

    def fetch_next(self):
        article_idx = self._queue.get()
        article_name = self._idxm.get_name(article_idx)

        assert article_name is not None
        print(f"-> [{article_name!r}]")

        return self._session.get(f"{BASE_URL}/{quote(article_name)}")

    def extend(self, entries):
        added = 0

        for entry in entries:
            if entry in self._idxm:
                continue

            i = self._idxm.add(entry)
            self._queue.put(i)
            added += 1

        print(f"Added {added} new articles")