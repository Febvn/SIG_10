import os
import sys
import math
import requests
import rasterio
from rasterio.transform import from_bounds
import numpy as np
from PIL import Image
import io

# Fix PROJ_LIB/GDAL_DATA conflicts on Windows
venv_base = os.path.dirname(os.path.abspath(__file__))
proj_data = os.path.join(venv_base, ".venv", "Lib", "site-packages", "rasterio", "proj_data")
gdal_data = os.path.join(venv_base, ".venv", "Lib", "site-packages", "rasterio", "gdal_data")

if os.path.exists(proj_data):
    os.environ['PROJ_LIB'] = proj_data
if os.path.exists(gdal_data):
    os.environ['GDAL_DATA'] = gdal_data


def deg2num(lat_deg, lon_deg, zoom_level):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom_level
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int(
        (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)
        / 2.0 * n
    )
    return xtile, ytile


def num2deg(xtile, ytile, zoom_level):
    n = 2.0 ** zoom_level
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def build_tile_url(zoom_level, ytile, xtile):
    base = "https://server.arcgisonline.com/ArcGIS/rest/services"
    return base + "/World_Imagery/MapServer/tile/" + str(zoom_level) + "/" + str(ytile) + "/" + str(xtile)


def download_tile(lat, lon, zoom_level, filename):
    xtile, ytile = deg2num(lat, lon, zoom_level)
    url = build_tile_url(zoom_level, ytile, xtile)

    print("Downloading " + filename + "...")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content)).convert('RGB')
            img_array = np.array(img)

            lat_top, lon_left = num2deg(xtile, ytile, zoom_level)
            lat_bottom, lon_right = num2deg(xtile + 1, ytile + 1, zoom_level)

            transform = from_bounds(lon_left, lat_bottom, lon_right, lat_top, img.width, img.height)

            with rasterio.open(
                filename,
                'w',
                driver='GTiff',
                height=img.height,
                width=img.width,
                count=3,
                dtype=img_array.dtype,
                crs='EPSG:4326',
                transform=transform,
            ) as dst:
                for i in range(3):
                    dst.write(img_array[:, :, i], i + 1)

            print("  Saved to " + filename)
            return True
        else:
            print("  Failed. Status code: " + str(response.status_code))
            return False
    except Exception as e:
        print("  Error downloading " + filename + ": " + str(e))
        return False


def generate_samples():
    locations = [
        {"name": "ITERA", "lat": -5.3582, "lon": 105.3148},
        {"name": "UNILA", "lat": -5.3650, "lon": 105.2440},
        {"name": "Tugu Adipura", "lat": -5.4165, "lon": 105.2584},
        {"name": "Bakauheni Port", "lat": -5.8710, "lon": 105.7530},
        {"name": "Airport Radin Inten", "lat": -5.2425, "lon": 105.1785},
        {"name": "Mall Bumi Kedaton", "lat": -5.3815, "lon": 105.2505},
        {"name": "Pusat Pemprov Lampung", "lat": -5.4350, "lon": 105.2750},
        {"name": "Stadion Pahoman", "lat": -5.4310, "lon": 105.2635},
        {"name": "Pantai Mutun Area", "lat": -5.5050, "lon": 105.2680},
        {"name": "Kawasan Industri Lematang", "lat": -5.3950, "lon": 105.3450}
    ]

    print("Starting batch download of 10 samples for Lampung...")

    success_count = 0
    for i, loc in enumerate(locations):
        filename = "lampung" + str(i + 1) + "_test_sample.tif"
        if download_tile(loc['lat'], loc['lon'], 18, filename):
            success_count += 1

    print("Batch complete! " + str(success_count) + "/10 files created.")


if __name__ == "__main__":
    generate_samples()
