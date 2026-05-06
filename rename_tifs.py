import os

mapping = {
    "lampung1_test_sample.tif": "lampung1_itera.tif",
    "lampung2_test_sample.tif": "lampung2_unila.tif",
    "lampung3_test_sample.tif": "lampung3_tanjungkarang.tif",
    "lampung4_test_sample.tif": "lampung4_bakauheni.tif",
    "lampung5_test_sample.tif": "lampung5_natar.tif",
    "lampung6_test_sample.tif": "lampung6_kedaton.tif",
    "lampung7_test_sample.tif": "lampung7_panjang.tif",
    "lampung8_test_sample.tif": "lampung8_telukbetung.tif",
    "lampung9_test_sample.tif": "lampung9_pulaupasaran.tif",
    "lampung10_test_sample.tif": "lampung10_wayhalim.tif",
    "lampung_test_sample.tif": "lampung_main_itera.tif"
}

folder = "data/tif_samples"

for old_name, new_name in mapping.items():
    old_path = os.path.join(folder, old_name)
    new_path = os.path.join(folder, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")
    else:
        print(f"File not found: {old_name}")
