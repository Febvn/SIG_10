import rasterio

with rasterio.open('lampung_test_sample.tif') as src:
    print("Bounds: " + str(src.bounds))
    print("CRS: " + str(src.crs))
    print("Transform: " + str(src.transform))
