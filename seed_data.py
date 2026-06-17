import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

sample_facilities = [
    {"nama": "Masjid Al-Anwar", "jenis": "Masjid", "alamat": "Jl. Teuku Umar No. 10, Bandar Lampung", "lon": 105.2677, "lat": -5.3971},
    {"nama": "SMAN 1 Bandar Lampung", "jenis": "Sekolah", "alamat": "Jl. Kartini No. 2, Bandar Lampung", "lon": 105.2622, "lat": -5.4292},
    {"nama": "Puskesmas Kedaton", "jenis": "Puskesmas", "alamat": "Jl. ZA Pagar Alam, Kedaton, Bandar Lampung", "lon": 105.2558, "lat": -5.3811},
    {"nama": "Indomaret Tanjung Karang", "jenis": "Minimarket", "alamat": "Jl. Raden Intan, Tanjung Karang", "lon": 105.2649, "lat": -5.4275},
    {"nama": "Taman Gajah", "jenis": "Taman", "alamat": "Jl. Teuku Umar, Way Halim, Bandar Lampung", "lon": 105.2707, "lat": -5.3920},
    {"nama": "Masjid Jami' Way Halim", "jenis": "Masjid", "alamat": "Jl. Imam Bonjol, Way Halim", "lon": 105.2580, "lat": -5.4050},
    {"nama": "SD Negeri 2 Enggal", "jenis": "Sekolah", "alamat": "Jl. Ikan Kakap, Enggal, Bandar Lampung", "lon": 105.2703, "lat": -5.4182},
    {"nama": "Puskesmas Tanjung Karang", "jenis": "Puskesmas", "alamat": "Jl. Raden Intan, Tanjung Karang Pusat", "lon": 105.2601, "lat": -5.4233},
    {"nama": "Alfamart Sukarame", "jenis": "Minimarket", "alamat": "Jl. Soekarno Hatta, Sukarame", "lon": 105.2890, "lat": -5.3755},
    {"nama": "Taman Hutan Raya", "jenis": "Taman", "alamat": "Jl. Wan Abdul Rahman, Bandar Lampung", "lon": 105.2455, "lat": -5.4088},
]

async def seed_database():
    print("Connecting to database...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Check if data already exists
        count = await conn.fetchval("SELECT COUNT(*) FROM fasilitas_publik")
        if count > 0:
            print(f"Database already has {count} facilities. Skipping seed.")
            return
        
        print("Inserting sample data...")
        for facility in sample_facilities:
            await conn.execute("""
                INSERT INTO fasilitas_publik (nama, jenis, alamat, geom)
                VALUES ($1, $2, $3, ST_SetSRID(ST_Point($4, $5), 4326))
            """, facility['nama'], facility['jenis'], facility['alamat'], facility['lon'], facility['lat'])
            print(f"  ✓ Added: {facility['nama']}")
        
        print(f"\n✅ Successfully seeded {len(sample_facilities)} facilities!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
