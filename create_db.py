import aiosqlite

import asyncio
from pathlib import Path

async def main():
    conn = await aiosqlite.connect(".db")
    script = Path("seeder.sql").read_text()

    try:
        await conn.executescript(script)
        await conn.commit()

    except Exception as e:
        print(e)

    finally:
        await conn.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())