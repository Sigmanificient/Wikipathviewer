import aiosqlite

from typing import Final


DB_PATH: Final[str] = ".db"


class Database:
    _conn = None

    @classmethod
    async def connect(cls):
        cls._conn = await aiosqlite.connect(DB_PATH)
        return cls()

    async def save_progress(self, current_id, current_name, children_ids):
        assert self._conn is not None

        await self._conn.execute(
            "INSERT INTO article(id, name) VALUES(?, ?)",
            (current_id, current_name)
        )

        for ref_id in children_ids:
            await self._conn.execute(
                "INSERT INTO ref(parent_article_id, article_id) VALUES(?, ?)",
                (current_id, ref_id)
            )

        await self._conn.commit()

    @classmethod
    async def close(cls):
        assert cls._conn is not None

        await cls._conn.close()
