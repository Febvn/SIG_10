import requests
import json

def test_detection():
    """Test detection API dengan sample TIF file"""
    
    # Path ke sample file
    sample_file = "data/tif_samples/lampung2_unila.tif"
    
    print(f"Testing detection with: {sample_file}")
    print("="*60)
    
    # Upload file ke API
    with open(sample_file, 'rb') as f:
        files = {'file': f}
        params = {
            'use_enhanced': 'true',
            'conf_threshold': '0.25',
            'visualize': 'false'
        }
        
        print("Sending request to API...")
        response = requests.post(
            'http://127.0.0.1:8000/detection/process',
            files=files,
            params=params,
            timeout=120
        )
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n✅ Detection Success!")
        print("="*60)
        
        # Check if response has geojson key
        if 'geojson' in result:
            geojson = result['geojson']
            detections_count = result.get('detections_count', 0)
        else:
            geojson = result
            detections_count = len(geojson.get('features', []))
        
        print(f"Total detections: {detections_count}")
        print(f"GeoJSON type: {geojson.get('type')}")
        print(f"Features count: {len(geojson.get('features', []))}")
        
        if geojson.get('features'):
            print("\nFirst 3 detections:")
            for i, feature in enumerate(geojson['features'][:3]):
                props = feature.get('properties', {})
                print(f"\n  Detection {i+1}:")
                print(f"    - Class: {props.get('class')}")
                print(f"    - Confidence: {props.get('confidence', 0)*100:.1f}%")
                print(f"    - Geometry: {feature.get('geometry', {}).get('type')}")
        
        # Save result untuk inspeksi
        with open('detection_test_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("\n📄 Full result saved to: detection_test_result.json")
        
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_detection()
