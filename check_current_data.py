import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def check_data():
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Get total count
        total = await conn.fetchval("SELECT COUNT(*) FROM fasilitas_publik")
        
        # Get count by category
        categories = await conn.fetch("""
            SELECT jenis, COUNT(*) as count 
            FROM fasilitas_publik 
            GROUP BY jenis 
            ORDER BY jenis
        """)
        
        # Get count by location (rough estimate based on coordinates)
        locations = await conn.fetch("""
            SELECT 
                CASE 
                    WHEN longitude BETWEEN 105.20 AND 105.30 AND latitude BETWEEN -5.50 AND -5.35 THEN 'Bandar Lampung'
                    WHEN longitude BETWEEN 105.29 AND 105.32 AND latitude BETWEEN -5.13 AND -5.10 THEN 'Metro'
                    WHEN longitude BETWEEN 105.55 AND 105.65 AND latitude BETWEEN -5.75 AND -5.70 THEN 'Lampung Selatan'
                    WHEN longitude BETWEEN 104.85 AND 104.92 AND latitude BETWEEN -4.85 AND -4.80 THEN 'Lampung Utara'
                    ELSE 'Other'
                END as location,
                COUNT(*) as count
            FROM fasilitas_publik
            GROUP BY location
            ORDER BY count DESC
        """)
        
        print("📊 CURRENT DATABASE STATUS")
        print("="*60)
        print(f"\n🏢 TOTAL FACILITIES: {total}")
        
        print("\n📋 BY CATEGORY:")
        print("-"*60)
        for cat in categories:
            print(f"   {cat['jenis']:<15} : {cat['count']}")
        
        print("\n🗺️  BY LOCATION (approximate):")
        print("-"*60)
        for loc in locations:
            print(f"   {loc['location']:<20} : {loc['count']}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_data())
