# 🎯 Panduan Training Model YOLO untuk Deteksi Wilayah

## 📋 Daftar Isi
1. [Persiapan Dataset](#persiapan-dataset)
2. [Labeling Data](#labeling-data)
3. [Training Model](#training-model)
4. [Evaluasi dan Testing](#evaluasi-dan-testing)
5. [Deployment](#deployment)

---

## 🗂️ Persiapan Dataset

### 1. Struktur Folder Dataset

```
dataset/
├── images/
│   ├── train/          # 70% dari data
│   ├── val/            # 20% dari data
│   └── test/           # 10% dari data
└── labels/
    ├── train/          # Label untuk training
    ├── val/            # Label untuk validation
    └── test/           # Label untuk testing
```

### 2. Setup Dataset Structure

```python
from prepare_dataset import DatasetPreparer

# Buat struktur folder otomatis
preparer = DatasetPreparer(output_dir='dataset')
```

### 3. Memotong Citra Besar

Jika Anda memiliki citra satelit yang sangat besar, potong menjadi tiles:

```python
# Potong citra besar menjadi tiles 640x640
preparer.split_large_image(
    image_path='data/tif_samples/lampung_large.tif',
    output_folder='dataset/temp',
    tile_size=640,
    overlap=100,
    prefix='lampung'
)
```

---

## 🏷️ Labeling Data

### Tools untuk Labeling

**Direkomendasikan:**
1. **LabelImg** - https://github.com/HumanSignal/labelImg
   - Mudah digunakan
   - Export langsung ke format YOLO
   
2. **Roboflow** - https://roboflow.com/
   - Online tool
   - Auto-augmentation
   - Export ke berbagai format

3. **CVAT** - https://www.cvat.ai/
   - Professional tool
   - Support team collaboration

### Format Label YOLO

**Standard Bounding Box:**
```
<class_id> <x_center> <y_center> <width> <height>
```
Semua nilai dinormalisasi (0-1)

**Contoh:**
```
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.15 0.2
```

### Definisi Class

Contoh untuk deteksi wilayah:
```yaml
names:
  0: wilayah_pemukiman
  1: wilayah_hutan
  2: wilayah_pertanian
  3: wilayah_industri
  4: wilayah_pesisir
```

### Membuat Label Manual

```python
# Contoh membuat label secara programmatic
bboxes = [
    (0, 100, 100, 300, 250),  # class_id=0, x1,y1,x2,y2
    (1, 350, 150, 500, 350),  # class_id=1, x1,y1,x2,y2
]

preparer.create_yolo_label(
    image_width=640,
    image_height=640,
    bboxes=bboxes,
    output_path='dataset/labels/train/image001.txt',
    format='xyxy'
)
```

### Verifikasi Label

```python
# Visualisasi label untuk memastikan benar
class_names = ['pemukiman', 'hutan', 'pertanian', 'industri']

preparer.visualize_labels(
    image_path='dataset/images/train/image001.jpg',
    label_path='dataset/labels/train/image001.txt',
    class_names=class_names,
    output_path='verification/image001_labeled.jpg'
)
```

---

## 🚀 Training Model

### 1. Split Dataset

```python
# Split otomatis train/val/test
preparer.split_dataset(
    images_folder='dataset/temp',
    labels_folder='dataset/temp_labels',
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1
)
```

### 2. Augmentasi Data (Opsional)

```python
# Perbanyak data dengan augmentasi
preparer.augment_image(
    image_path='dataset/images/train/image001.jpg',
    output_folder='dataset/images/train',
    num_augmentations=5
)
```

### 3. Training Basic

```python
from train_model import ModelTrainer

# Define classes
classes = ['wilayah_pemukiman', 'wilayah_hutan', 'wilayah_pertanian', 'wilayah_industri']

# Initialize trainer
trainer = ModelTrainer(model_size='s', task='detect')

# Create config
config_path = trainer.create_dataset_config(
    dataset_path='dataset',
    class_names=classes,
    output_file='dataset.yaml'
)

# Train model
results = trainer.train(
    data_yaml=config_path,
    epochs=100,
    imgsz=640,
    batch=16,
    patience=50,
    device='0'  # Gunakan '0' untuk GPU, 'cpu' untuk CPU
)
```

### 4. Training dengan Parameter Custom

```python
# Training dengan parameter lebih advanced
results = trainer.train(
    data_yaml=config_path,
    epochs=200,          # Lebih banyak epoch
    imgsz=640,
    batch=16,
    patience=100,        # Early stopping patience
    device='0',
    # Optimizer settings
    optimizer='AdamW',
    lr0=0.01,           # Learning rate awal
    lrf=0.01,           # Learning rate akhir
    # Augmentation settings
    hsv_h=0.015,        # Hue augmentation
    hsv_s=0.7,          # Saturation augmentation
    hsv_v=0.4,          # Value augmentation
    degrees=10.0,       # Rotation degree
    translate=0.1,      # Translation
    scale=0.5,          # Scale variation
    fliplr=0.5,         # Horizontal flip
    mosaic=1.0,         # Mosaic augmentation
)
```

### 5. Model Size Comparison

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| YOLOv8n | Nano | Fastest | Good |
| YOLOv8s | Small | Fast | Better |
| YOLOv8m | Medium | Medium | Good |
| YOLOv8l | Large | Slow | Excellent |
| YOLOv8x | XLarge | Slowest | Best |

**Rekomendasi:**
- **Development/Testing:** YOLOv8n (cepat)
- **Production (balanced):** YOLOv8s atau YOLOv8m
- **High Accuracy needed:** YOLOv8l atau YOLOv8x

---

## 📊 Evaluasi dan Testing

### 1. Validasi Model

```python
# Validasi setelah training
results = trainer.validate(data_yaml=config_path)

print(f"mAP50: {results.box.map50}")
print(f"mAP50-95: {results.box.map}")
```

### 2. Testing pada Gambar Baru

```python
from detection.detector_enhanced import EnhancedSatelliteDetector

# Load trained model
detector = EnhancedSatelliteDetector(
    model_path='runs/train/exp/weights/best.pt',
    conf_threshold=0.25
)

# Test dengan visualisasi
geojson_result, detections = detector.run_detection(
    image_path='test_image.tif',
    visualize=True,
    output_path='test_result.jpg'
)

print(f"Terdeteksi: {len(detections)} objek")
```

### 3. Metrics Evaluation

```python
# Lihat metrics training
import pandas as pd

# Load results CSV
df = pd.read_csv('runs/train/exp/results.csv')

# Plot metrics
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot(df['train/box_loss'], label='Train')
plt.plot(df['val/box_loss'], label='Val')
plt.title('Box Loss')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(df['metrics/mAP50(B)'])
plt.title('mAP50')

plt.subplot(1, 3, 3)
plt.plot(df['metrics/mAP50-95(B)'])
plt.title('mAP50-95')

plt.tight_layout()
plt.savefig('training_metrics.png')
```

---

## 🚢 Deployment

### 1. Export Model

```python
# Export ke format lain
trainer.export_model(format='onnx')  # ONNX
# trainer.export_model(format='tflite')  # TensorFlow Lite
# trainer.export_model(format='torchscript')  # TorchScript
```

### 2. Update Model di API

Ganti model di `detection/detector.py` atau `detection/detector_enhanced.py`:

```python
detector = EnhancedSatelliteDetector(
    model_path='runs/train/exp/weights/best.pt',  # Model hasil training
    conf_threshold=0.25,
    iou_threshold=0.45
)
```

### 3. Test API Endpoint

```bash
# Test dengan curl
curl -X POST "http://localhost:8000/detection/process?use_enhanced=true&visualize=true" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.tif"
```

---

## 💡 Tips untuk Akurasi Lebih Baik

### 1. Dataset Quality
- ✅ Minimal 100-200 gambar per class
- ✅ Variasi kondisi (siang/malam, musim berbeda)
- ✅ Label yang akurat dan konsisten
- ✅ Balance antara classes

### 2. Augmentation
- Gunakan augmentasi untuk perbanyak data
- Rotasi, flip, brightness, contrast variation
- Mosaic augmentation sangat efektif

### 3. Training Tips
- Mulai dengan model kecil (YOLOv8n) untuk cepat iterasi
- Gunakan early stopping (patience parameter)
- Monitor validation loss, jangan overfit
- Fine-tune dengan learning rate yang lebih kecil

### 4. Hyperparameter Tuning
```python
# Auto hyperparameter tuning
from ultralytics import YOLO

model = YOLO('yolov8s.pt')
model.tune(
    data='dataset.yaml',
    epochs=30,
    iterations=300,
    optimizer='AdamW',
    plots=True,
    save=True
)
```

### 5. Post-Processing
- Adjust confidence threshold berdasarkan use case
- Gunakan NMS (Non-Maximum Suppression) yang tepat
- Filter deteksi berdasarkan area minimum

---

## 🐛 Troubleshooting

### Error: CUDA out of memory
```python
# Kurangi batch size
trainer.train(batch=8)  # atau lebih kecil
```

### Error: No detections
- Cek confidence threshold (turunkan ke 0.1)
- Verify label format benar
- Pastikan model sudah trained dengan baik

### Poor Performance
- Tambah data training
- Increase epochs
- Try larger model (YOLOv8m atau YOLOv8l)
- Improve label quality

---

## 📚 Resources

- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **Roboflow Guide:** https://blog.roboflow.com/how-to-train-yolov8-on-a-custom-dataset/
- **Dataset Collection:** 
  - https://public.roboflow.com/
  - https://universe.roboflow.com/

---

## 🎓 Next Steps

1. ✅ Kumpulkan dan label dataset Anda
2. ✅ Train model dengan script yang disediakan
3. ✅ Evaluasi dan fine-tune
4. ✅ Deploy ke production
5. ✅ Monitor performance dan retrain jika perlu

---

**Happy Training! 🚀**
