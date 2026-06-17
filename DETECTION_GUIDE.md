# 🎯 Panduan Object Detection - WebGIS Bandar Lampung

## Overview
Fitur Object Detection menggunakan YOLOv8 untuk mendeteksi objek secara otomatis dari citra satelit wilayah Bandar Lampung.

## 📋 Supported File Formats
- **GeoTIFF** (.tif, .tiff) - Recommended
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)

## 🚀 Cara Menggunakan

### Melalui Frontend (Web UI)

1. **Buka Aplikasi**
   - Akses: http://localhost:5173/

2. **Aktifkan Mode Detection**
   - Klik tombol **"Detect"** di sidebar
   - UI akan menampilkan form upload

3. **Upload Gambar**
   - Klik tombol **"Upload & Detect"**
   - Pilih file TIF/JPG/PNG dari komputer Anda
   - Tunggu proses detection (bisa memakan waktu 10-60 detik tergantung ukuran gambar)

4. **Lihat Hasil**
   - Peta akan otomatis zoom ke area yang terdeteksi
   - Bounding box **merah** akan muncul di setiap objek
   - Label objek akan ditampilkan di atas bounding box
   - Klik bounding box untuk melihat detail (class & confidence)

### Melalui API (Backend)

#### Endpoint
```
POST http://127.0.0.1:8000/detection/process
```

#### Parameters
- `file` (required): Image file to process
- `use_enhanced` (optional, default: false): Use enhanced detector
- `conf_threshold` (optional, default: 0.25): Confidence threshold (0.0-1.0)
- `visualize` (optional, default: false): Generate visualization image

#### Example dengan curl:
```bash
curl -X POST "http://127.0.0.1:8000/detection/process?use_enhanced=true&conf_threshold=0.25" \
  -F "file=@data/tif_samples/lampung2_unila.tif"
```

#### Example dengan Python:
```python
import requests

with open('lampung_image.tif', 'rb') as f:
    files = {'file': f}
    params = {
        'use_enhanced': 'true',
        'conf_threshold': '0.25'
    }
    response = requests.post(
        'http://127.0.0.1:8000/detection/process',
        files=files,
        params=params
    )
    result = response.json()
    print(f"Detected {result['detections_count']} objects")
```

#### Response Format:
```json
{
  "geojson": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [...]
        },
        "properties": {
          "class": "roundabout",
          "confidence": 0.8824,
          "type": "obb"
        }
      }
    ]
  },
  "detections_count": 1
}
```

## 🎨 Tampilan di Peta

### Bounding Box
- **Warna**: Merah (#ef4444)
- **Style**: Dashed line
- **Fill**: Semi-transparent merah

### Label
- **Posisi**: Di tengah bounding box
- **Animasi**: Pulse effect
- **Format**: 🎯 [CLASS_NAME]

### Popup
- **Trigger**: Klik pada bounding box
- **Konten**:
  - 🎯 Icon
  - Nama class objek
  - Confidence percentage

## 🧪 Testing Detection

### Test dengan Sample Files
Sample files tersedia di: `data/tif_samples/`

Files:
- lampung2_unila.tif (Area ITERA)
- lampung3_tanjungkarang.tif (Tanjung Karang)
- lampung4_bakauheni.tif (Bakauheni)
- lampung5_natar.tif (Natar)
- lampung8_telukbetung.tif (Teluk Betung)

### Test Script
Jalankan script test:
```bash
python test_detection_api.py
```

Output akan disimpan di: `detection_test_result.json`

## 🔧 Konfigurasi

### Confidence Threshold
- **Default**: 0.25 (25%)
- **Range**: 0.0 - 1.0
- **Rekomendasi**:
  - 0.1-0.2: Banyak deteksi, lebih banyak false positive
  - 0.25-0.3: Balanced (recommended)
  - 0.4-0.5: Lebih sedikit deteksi, lebih akurat

### Model
- **Current**: YOLOv8n-OBB (Oriented Bounding Box)
- **Location**: `yolov8n-obb.pt`
- Model akan auto-download saat pertama kali digunakan

## 📦 Dependencies
```
ultralytics
rasterio
opencv-python
numpy
geojson
```

## 🐛 Troubleshooting

### Error: "Detection failed"
- Pastikan file format benar (TIF/JPG/PNG)
- Cek ukuran file tidak terlalu besar (max recommended: 50MB)
- Pastikan file memiliki geo-coordinates (untuk TIF)

### Tidak ada objek terdeteksi
- Turunkan confidence threshold
- Pastikan gambar cukup jelas dan resolusi bagus
- Cek apakah objek dalam gambar termasuk class yang bisa dideteksi model

### Bounding box tidak muncul di peta
- Pastikan basemap sudah switch ke satellite
- Refresh browser
- Cek console browser untuk error

## 🎓 Classes yang Dapat Dideteksi

Model YOLOv8-OBB dapat mendeteksi berbagai objek dalam citra satelit, termasuk:
- Buildings
- Roads
- Roundabouts
- Parking lots
- Vehicles
- Trees/Vegetation
- Dan lainnya...

## 📝 Notes

1. **Performance**: Detection membutuhkan waktu tergantung:
   - Ukuran gambar
   - Jumlah objek
   - Hardware server

2. **Accuracy**: Akurasi tergantung:
   - Kualitas gambar
   - Resolusi
   - Kondisi pencahayaan
   - Training data model

3. **Geo-coordinates**: 
   - Untuk TIF dengan geo-transform, koordinat akan akurat
   - Untuk JPG/PNG tanpa geo-info, akan menggunakan pixel coordinates
