import asyncio
import asyncpg

async def create_database():
    # Connect to default postgres database
    conn = await asyncpg.connect(
        user='postgres',
        password='admin123',
        host='localhost',
        port=5432,
        database='postgres'
    )
    
    try:
        # Check if database exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = 'db_gis_itera'"
        )
        
        if exists:
            print("Database 'db_gis_itera' already exists.")
        else:
            # Create database (need to use isolation level)
            await conn.execute('CREATE DATABASE db_gis_itera')
            print("Database 'db_gis_itera' created successfully!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_database())
