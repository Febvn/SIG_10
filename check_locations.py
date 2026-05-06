import rasterio
import os
import json

def get_tif_info(folder_path):
    results = []
    files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]
    
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        try:
            with rasterio.open(file_path) as src:
                bounds = src.bounds
                center_lon = (bounds.left + bounds.right) / 2
                center_lat = (bounds.bottom + bounds.top) / 2
                
                results.append({
                    "filename": filename,
                    "bounds": {
                        "left": bounds.left,
                        "bottom": bounds.bottom,
                        "right": bounds.right,
                        "top": bounds.top
                    },
                    "center": {
                        "lat": center_lat,
                        "lon": center_lon
                    },
                    "crs": str(src.crs),
                    "width": src.width,
                    "height": src.height
                })
        except Exception as e:
            results.append({"filename": filename, "error": str(e)})
            
    return results

if __name__ == "__main__":
    folder = "data/tif_samples"
    info = get_tif_info(folder)
    print(json.dumps(info, indent=4))
    
    with open("data/tif_locations.json", "w") as f:
        json.dump(info, f, indent=4)
