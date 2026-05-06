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

        # Check table
        rows = await conn.fetch("SELECT id, nama, jenis FROM fasilitas_publik LIMIT 5")
        if rows:
            print("Found " + str(len(rows)) + " records in 'fasilitas_publik':")
            for r in rows:
                print(" - ID: " + str(r['id']) + ", Nama: " + str(r['nama']) + ", Jenis: " + str(r['jenis']))
        else:
            print("Table 'fasilitas_publik' exists but is empty.")

        await conn.close()
    except Exception as e:
        print("FAILED: " + str(e))


if __name__ == "__main__":
    asyncio.run(test())
