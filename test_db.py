import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


async def test():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("SUCCESS: Connected to database!")
        await conn.close()
    except Exception as e:
        print("FAILED: " + str(e))


if __name__ == "__main__":
    asyncio.run(test())
