# 🎯 Enhanced Object Detection Training System

Sistem training yang ditingkatkan untuk deteksi wilayah menggunakan YOLOv8 dengan visualisasi bounding box yang lebih baik.

## 🚀 Fitur Baru

### 1. **Enhanced Detector** (`detection/detector_enhanced.py`)
- ✅ Visualisasi bounding box dengan warna per class
- ✅ Label confidence score pada setiap deteksi
- ✅ Semi-transparent polygon overlay
- ✅ Configurable confidence dan IOU threshold
- ✅ Support untuk standard box dan oriented bounding box (OBB)

### 2. **Training System** (`train_model.py`)
- ✅ Multiple model sizes (nano, small, medium, large, xlarge)
- ✅ Advanced augmentations untuk akurasi lebih tinggi
- ✅ Auto dataset configuration
- ✅ Early stopping dengan patience
- ✅ Model export ke berbagai format (ONNX, TFLite, dll)
- ✅ Hyperparameter optimization

### 3. **Dataset Preparation** (`prepare_dataset.py`)
- ✅ Auto split large images menjadi tiles
- ✅ Auto train/val/test split
- ✅ Label visualization untuk verifikasi
- ✅ Data augmentation tools
- ✅ YOLO format label creation

### 4. **Enhanced API** (`routers/detection.py`)
- ✅ Parameter `use_enhanced` untuk detector yang lebih baik
- ✅ Configurable confidence threshold
- ✅ Visualization output (base64 encoded)
- ✅ Detection count dan metadata

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download pre-trained YOLO models (otomatis saat pertama kali digunakan)
# yolov8n.pt, yolov8s.pt, yolov8m.pt, dll akan didownload otomatis
```

## 🎓 Quick Start Training

### Option 1: Quick Start Script (Recommended untuk pemula)

```bash
python quick_start_training.py
```

Script ini akan:
1. Setup struktur dataset
2. Guide Anda melalui konfigurasi
3. Mulai training dengan parameter optimal
4. Validate model setelah training

### Option 2: Manual Training (Advanced)

```python
from train_model import ModelTrainer

# 1. Define classes
classes = [
    'wilayah_pemukiman',
    'wilayah_hutan', 
    'wilayah_pertanian',
    'wilayah_industri'
]

# 2. Initialize trainer
trainer = ModelTrainer(model_size='s', task='detect')

# 3. Create dataset config
config_path = trainer.create_dataset_config(
    dataset_path='dataset',
    class_names=classes
)

# 4. Train
results = trainer.train(
    data_yaml=config_path,
    epochs=100,
    imgsz=640,
    batch=16,
    device='0'  # GPU
)

# 5. Validate
trainer.validate(data_yaml=config_path)
```

## 🗂️ Dataset Preparation

### Struktur Dataset

```
dataset/
├── images/
│   ├── train/      # 70% data training
│   ├── val/        # 20% data validasi
│   └── test/       # 10% data testing
└── labels/
    ├── train/      # Label untuk training
    ├── val/        # Label untuk validasi
    └── test/       # Label untuk testing
```

### Prepare Dataset

```python
from prepare_dataset import DatasetPreparer

preparer = DatasetPreparer()

# 1. Split large satellite image
preparer.split_large_image(
    image_path='large_image.tif',
    output_folder='dataset/temp',
    tile_size=640,
    overlap=100
)

# 2. Split into train/val/test
preparer.split_dataset(
    images_folder='dataset/temp',
    labels_folder='dataset/temp_labels',
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1
)

# 3. Visualize labels (untuk verifikasi)
preparer.visualize_labels(
    image_path='dataset/images/train/image001.jpg',
    label_path='dataset/labels/train/image001.txt',
    class_names=['class1', 'class2'],
    output_path='verification/image001.jpg'
)
```

## 🧪 Testing Trained Model

### Test Single Image

```bash
python test_trained_model.py --image test_image.tif
```

### Test Multiple Images (Batch)

```bash
python test_trained_model.py --folder data/tif_samples/
```

### Test with Custom Parameters

```bash
python test_trained_model.py \
    --image test.tif \
    --model runs/train/exp/weights/best.pt \
    --conf 0.3 \
    --output results/
```

### Programmatic Testing

```python
from detection.detector_enhanced import EnhancedSatelliteDetector

# Load your trained model
detector = EnhancedSatelliteDetector(
    model_path='runs/train/exp/weights/best.pt',
    conf_threshold=0.25,
    iou_threshold=0.45
)

# Run detection with visualization
geojson_result, detections = detector.run_detection(
    image_path='test_image.tif',
    visualize=True,
    output_path='result_with_boxes.jpg'
)

print(f"Detected {len(detections)} objects")
for det in detections:
    print(f"  - {det['class_name']}: {det['score']:.2f}")
```

## 🌐 Using in API

### Start API Server

```bash
cd SIG_10
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

#### 1. Standard Detection
```bash
curl -X POST "http://localhost:8000/detection/process" \
  -F "file=@image.tif"
```

#### 2. Enhanced Detection with Visualization
```bash
curl -X POST "http://localhost:8000/detection/process?use_enhanced=true&visualize=true&conf_threshold=0.25" \
  -F "file=@image.tif"
```

Response:
```json
{
  "geojson": {...},
  "detections_count": 45,
  "visualization": "base64_encoded_image...",
  "visualization_format": "base64_jpeg"
}
```

#### 3. Get Available Classes
```bash
curl "http://localhost:8000/detection/classes"
```

### Update API to Use Trained Model

Edit `routers/detection.py`:

```python
enhanced_detector = EnhancedSatelliteDetector(
    model_path='runs/train/exp/weights/best.pt',  # Your trained model
    conf_threshold=0.25,
    iou_threshold=0.45
)
```

## 📊 Model Comparison

| Model | Size (MB) | Speed | mAP50 | Best Use Case |
|-------|-----------|-------|-------|---------------|
| YOLOv8n | 6 | ⚡⚡⚡⚡⚡ | ~37% | Development/Testing |
| YOLOv8s | 22 | ⚡⚡⚡⚡ | ~45% | **Production (Balanced)** |
| YOLOv8m | 52 | ⚡⚡⚡ | ~50% | High Accuracy Needed |
| YOLOv8l | 87 | ⚡⚡ | ~53% | Maximum Accuracy |
| YOLOv8x | 136 | ⚡ | ~54% | Research/Benchmark |

**Rekomendasi:**
- Untuk **development**: YOLOv8n (cepat iterasi)
- Untuk **production**: YOLOv8s atau YOLOv8m (balance speed-accuracy)
- Untuk **research**: YOLOv8l atau YOLOv8x (maximum accuracy)

## 🎨 Visualization Examples

### Before Training
- Model pre-trained dari COCO dataset
- Deteksi generic objects (person, car, dll)
- Tidak spesifik untuk wilayah

### After Training
- Model di-train dengan data custom Anda
- Deteksi wilayah spesifik (pemukiman, hutan, pertanian, dll)
- Bounding box dengan label dan confidence score
- Color-coded per class

## 💡 Tips untuk Hasil Terbaik

### 1. Data Quality
- **Minimum**: 100-200 gambar per class
- **Ideal**: 500-1000+ gambar per class
- **Variasi**: Berbagai kondisi (cuaca, waktu, sudut)
- **Balance**: Jumlah sample seimbang antar class

### 2. Labeling
- Gunakan tools profesional (LabelImg, Roboflow, CVAT)
- Konsisten dalam labeling
- Include border objects (jangan hanya object di tengah)
- Verify labels dengan visualization

### 3. Training
- **Start small**: Mulai dengan YOLOv8n untuk cepat
- **Monitor**: Watch training curves, prevent overfitting
- **Patience**: Gunakan early stopping
- **Fine-tune**: Adjust learning rate jika perlu

### 4. Augmentation
- Flip (horizontal)
- Rotation (kecil saja, 0-10 derajat)
- HSV variation (brightness, saturation)
- Mosaic augmentation (sangat efektif!)

### 5. Post-Training
- Test pada data yang belum pernah dilihat
- Adjust confidence threshold sesuai use case
- Consider ensemble models untuk akurasi lebih tinggi

## 🐛 Troubleshooting

### Problem: CUDA out of memory
**Solution**: Kurangi batch size
```python
trainer.train(batch=8)  # atau 4, 2
```

### Problem: No detections
**Solutions**:
- Turunkan confidence threshold ke 0.1
- Check label format benar (normalized 0-1)
- Verify model trained properly (check mAP)

### Problem: Low accuracy
**Solutions**:
- Tambah lebih banyak data training
- Improve label quality
- Try model yang lebih besar (YOLOv8m/l)
- Increase epochs (100 → 200)
- Check data augmentation

### Problem: Overfitting
**Solutions**:
- Reduce epochs
- Increase patience for early stopping
- Add more augmentation
- Add more training data

## 📚 Documentation

- **TRAINING_GUIDE.md**: Panduan lengkap training (BACA INI!)
- **README.md**: Main project documentation
- **YOLOv8 Official Docs**: https://docs.ultralytics.com/

## 🔧 Advanced Features

### Hyperparameter Tuning

```python
from ultralytics import YOLO

model = YOLO('yolov8s.pt')
model.tune(
    data='dataset.yaml',
    epochs=30,
    iterations=300,
    optimizer='AdamW'
)
```

### Export to Different Formats

```python
trainer.export_model(format='onnx')     # ONNX
trainer.export_model(format='tflite')   # TensorFlow Lite
trainer.export_model(format='coreml')   # CoreML (iOS)
```

### Custom Augmentation

```python
results = trainer.train(
    data_yaml=config_path,
    # Custom augmentation parameters
    degrees=10.0,      # Rotation
    translate=0.1,     # Translation
    scale=0.5,         # Scale
    shear=2.0,         # Shear
    perspective=0.0,   # Perspective
    flipud=0.0,        # Vertical flip
    fliplr=0.5,        # Horizontal flip
    mosaic=1.0,        # Mosaic
    mixup=0.1,         # Mixup
)
```

## 📈 Performance Metrics

Training menghasilkan metrics:
- **Precision**: Seberapa akurat prediksi positive
- **Recall**: Seberapa banyak object yang terdeteksi
- **mAP50**: Mean Average Precision @ IoU 0.5
- **mAP50-95**: mAP pada berbagai IoU threshold

**Target yang baik:**
- mAP50 > 0.5 (50%)
- mAP50-95 > 0.35 (35%)

## 🎯 Next Steps

1. ✅ Prepare dataset Anda (images + labels)
2. ✅ Run `python quick_start_training.py`
3. ✅ Evaluate dengan `python test_trained_model.py`
4. ✅ Deploy ke API dengan update model path
5. ✅ Monitor performance dan retrain jika perlu

## 📞 Support

Jika ada pertanyaan atau issues:
1. Baca **TRAINING_GUIDE.md** untuk panduan detail
2. Check troubleshooting section di atas
3. Refer ke YOLOv8 official documentation

---

**Happy Training! 🚀**

*System ini menggunakan YOLOv8 dari Ultralytics dengan enhancement khusus untuk satellite imagery detection.*
