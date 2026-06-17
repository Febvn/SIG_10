import requests
import json

def test_nearby():
    """Test nearby API di area Tanjung Karang"""
    
    # Koordinat SMAN 1 Bandar Lampung (Tanjung Karang)
    lat = -5.4292
    lon = 105.2622
    radius = 2000  # 2 km
    
    print("🗺️  TESTING NEARBY API")
    print("="*60)
    print(f"📍 Location: Tanjung Karang ({lat}, {lon})")
    print(f"📏 Radius: {radius}m ({radius/1000}km)")
    print("="*60)
    
    # Call API
    url = f"http://127.0.0.1:8000/fasilitas/nearby?lat={lat}&lon={lon}&radius={radius}"
    response = requests.get(url)
    
    if response.status_code == 200:
        facilities = response.json()
        
        # Count by category
        categories = {}
        for f in facilities:
            jenis = f['jenis']
            categories[jenis] = categories.get(jenis, 0) + 1
        
        print(f"\n✅ Found {len(facilities)} facilities within {radius}m!")
        print("\n📊 BREAKDOWN BY CATEGORY:")
        print("-"*60)
        for category, count in sorted(categories.items()):
            print(f"   {category.upper():<15} : {count}")
        
        print("\n📋 TOP 10 CLOSEST FACILITIES:")
        print("-"*60)
        for i, f in enumerate(facilities[:10], 1):
            jarak_km = f['jarak'] / 1000
            print(f"{i:2}. [{f['jenis']:<12}] {f['nama']:<40} - {jarak_km:.2f}km")
        
        # Save full result
        with open('nearby_test_result.json', 'w', encoding='utf-8') as file:
            json.dump(facilities, file, indent=2, ensure_ascii=False)
        
        print("\n📄 Full result saved to: nearby_test_result.json")
        print("\n✅ API TEST SUCCESSFUL!")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_nearby()
