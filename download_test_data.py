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


def download_lampung_sample():
    # Airport Radin Inten II - Area Pesawat
    lat_center = -5.2425
    lon_center = 105.1785
    zoom_level = 18

    xtile, ytile = deg2num(lat_center, lon_center, zoom_level)
    url = build_tile_url(zoom_level, ytile, xtile)

    print("Downloading satellite tile...")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print("Gagal mendownload. Status code: " + str(response.status_code))
            return

        img = Image.open(io.BytesIO(response.content)).convert('RGB')
        img_array = np.array(img)

        lat_top, lon_left = num2deg(xtile, ytile, zoom_level)
        lat_bottom, lon_right = num2deg(xtile + 1, ytile + 1, zoom_level)

        output_path = "lampung_test_sample.tif"
        transform = from_bounds(lon_left, lat_bottom, lon_right, lat_top, img.width, img.height)

        with rasterio.open(
            output_path,
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

        print("File berhasil disimpan ke: " + os.path.abspath(output_path))

    except Exception as e:
        print("Error saat download: " + str(e))


if __name__ == "__main__":
    download_lampung_sample()
