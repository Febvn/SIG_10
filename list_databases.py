import asyncio
import asyncpg

async def list_databases():
    # Connect to default postgres database
    conn = await asyncpg.connect(
        user='postgres',
        password='admin123',
        host='localhost',
        port=5432,
        database='postgres'
    )
    
    try:
        # Query to list all databases
        databases = await conn.fetch("""
            SELECT datname as "Name", 
                   pg_catalog.pg_get_userbyid(datdba) as "Owner",
                   pg_catalog.pg_encoding_to_char(encoding) as "Encoding"
            FROM pg_catalog.pg_database
            ORDER BY datname;
        """)
        
        print("\n" + "="*60)
        print("List of databases:")
        print("="*60)
        print(f"{'Name':<20} {'Owner':<15} {'Encoding':<15}")
        print("-"*60)
        
        for db in databases:
            print(f"{db['Name']:<20} {db['Owner']:<15} {db['Encoding']:<15}")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(list_databases())
