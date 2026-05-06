from PIL import Image
import rasterio
import numpy as np
import os


def convert_tif_to_jpg(tif_path, jpg_path):
    print("Converting " + tif_path + " to " + jpg_path + "...")
    try:
        with rasterio.open(tif_path) as src:
            # Read the bands (RGB)
            img = src.read([1, 2, 3])
            # Reshape from (count, height, width) to (height, width, count)
            img = np.moveaxis(img, 0, -1)

            # Create PIL image
            pil_img = Image.fromarray(img.astype('uint8'))
            pil_img.save(jpg_path, "JPEG", quality=95)
            print("  Successfully saved to " + os.path.abspath(jpg_path))
            print("  Note: This JPG file DOES NOT contain geographic coordinates.")
    except Exception as e:
        print("  Error: " + str(e))


if __name__ == "__main__":
    convert_tif_to_jpg('lampung1_test_sample.tif', 'lampung1_itera_no_geo.jpg')
