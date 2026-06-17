# ⚡ QUICK START - Training Model untuk Deteksi Wilayah

Panduan singkat untuk mulai training model deteksi wilayah dengan bounding box.

## 🚀 Langkah Cepat (5 Steps)

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Buat Dataset dari GeoTIFF

```bash
# Letakkan file TIF Anda di data/tif_samples/
python create_sample_dataset.py --input data/tif_samples --output dataset
```

Ini akan:
- ✅ Memotong GeoTIFF menjadi tiles 640x640
- ✅ Split menjadi train/val/test (70/20/10)
- ✅ Buat struktur folder yang benar

### 3️⃣ Label Data Anda

**Pilih salah satu tool:**

**Option A: LabelImg (Recommended - Offline)**
```bash
pip install labelImg
labelImg dataset/images/train dataset/classes.txt
```

**Option B: Roboflow (Online)**
- Upload ke https://roboflow.com/
- Label secara online
- Export sebagai "YOLOv8" format

**Option C: CVAT (Professional)**
- Deploy CVAT: https://www.cvat.ai/
- Import images
- Create annotations

**Format Label:**
```
<class_id> <x_center> <y_center> <width> <height>
```
Contoh:
```
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.15 0.2
```

### 4️⃣ Training Model

```bash
python quick_start_training.py
```

Pilihan cepat dalam script:
- Model size: 's' (small - recommended)
- Epochs: 100
- Batch: 16
- Device: '0' (GPU) atau 'cpu'

**Custom training:**
```python
from train_model import ModelTrainer

trainer = ModelTrainer(model_size='s', task='detect')
trainer.train(
    data_yaml='dataset/dataset.yaml',
    epochs=100,
    batch=16,
    device='0'
)
```

### 5️⃣ Test Model

```bash
# Test single image
python test_trained_model.py --image test.tif

# Test multiple images
python test_trained_model.py --folder data/tif_samples/

# Compare before/after training
python demo_detection.py test.tif
```

---

## 📊 Visual Workflow

```
GeoTIFF Files                Dataset                  Labeled Dataset
    │                           │                           │
    │  create_sample_dataset    │    LabelImg/Roboflow      │
    └───────────────────────────┤───────────────────────────┤
                                │                           │
                          dataset/images/            dataset/labels/
                          ├── train/                 ├── train/
                          ├── val/                   ├── val/
                          └── test/                  └── test/
                                │                           │
                                │    quick_start_training   │
                                └───────────────────────────┤
                                                            │
                                                     Trained Model
                                                  runs/train/exp/weights/best.pt
                                                            │
                                                            │  test_trained_model
                                                            └──────────────────────>
                                                         Detection Results with Boxes!
```

---

## 🎯 Contoh Classes untuk Deteksi Wilayah

Edit `dataset/classes_example.txt`:

```yaml
# Deteksi Wilayah
wilayah_pemukiman
wilayah_hutan
wilayah_pertanian
wilayah_industri
wilayah_pesisir

# Atau deteksi bangunan
bangunan_rumah
bangunan_gedung
bangunan_pabrik
jalan
sawah

# Atau custom sesuai kebutuhan
kelas_a
kelas_b
kelas_c
```

---

## 📁 Struktur Files

```
SIG_10/
├── 📘 Quick References
│   ├── QUICKSTART.md              ← You are here
│   ├── README_TRAINING.md         ← Full training system docs
│   └── TRAINING_GUIDE.md          ← Detailed training guide
│
├── 🚀 Main Scripts
│   ├── quick_start_training.py    ← Start here!
│   ├── test_trained_model.py      ← Test your model
│   ├── demo_detection.py          ← Compare before/after
│   └── create_sample_dataset.py   ← Prepare dataset
│
├── 🔧 Core Modules
│   ├── train_model.py             ← Training system
│   ├── prepare_dataset.py         ← Dataset utilities
│   └── detection/
│       ├── detector.py            ← Original detector
│       └── detector_enhanced.py   ← Enhanced with visualization
│
└── 📊 Dataset & Results
    ├── dataset/                   ← Your training data
    ├── runs/train/                ← Training results
    └── test_results/              ← Test outputs
```

---

## 💡 Tips Cepat

### Dataset Quality
- **Minimum**: 50-100 images per class
- **Better**: 200-500 images per class
- **Best**: 1000+ images per class

### Model Selection
| Use Case | Model | Speed | Accuracy |
|----------|-------|-------|----------|
| Development | YOLOv8n | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ |
| Production | YOLOv8s | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| High Accuracy | YOLOv8m | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |

### Training Time Estimates
- YOLOv8n (100 epochs, 500 images): ~30-60 min (GPU)
- YOLOv8s (100 epochs, 500 images): ~1-2 hours (GPU)
- YOLOv8m (100 epochs, 500 images): ~2-4 hours (GPU)

---

## 🐛 Common Issues

### Issue: CUDA out of memory
```python
# Solution: Reduce batch size
trainer.train(batch=8)  # or 4, 2
```

### Issue: No detections after training
```python
# Solution: Lower confidence threshold
detector.run_detection(conf=0.1)
```

### Issue: Training too slow
```bash
# Use smaller model
python quick_start_training.py  # Choose 'n' instead of 's'
```

---

## 🌐 Deploy to API

After training, update `routers/detection.py`:

```python
enhanced_detector = EnhancedSatelliteDetector(
    model_path='runs/train/exp/weights/best.pt',  # Your trained model
    conf_threshold=0.25
)
```

Test API:
```bash
# Start server
uvicorn main:app --reload

# Test endpoint
curl -X POST "http://localhost:8000/detection/process?use_enhanced=true&visualize=true" \
  -F "file=@test_image.tif"
```

---

## 📚 Learn More

- **TRAINING_GUIDE.md**: Detailed training tutorial
- **README_TRAINING.md**: Complete system documentation
- **YOLOv8 Docs**: https://docs.ultralytics.com/

---

## 🎓 Complete Workflow Example

```bash
# 1. Setup
pip install -r requirements.txt

# 2. Prepare dataset
python create_sample_dataset.py

# 3. Label data (using LabelImg or Roboflow)
labelImg dataset/images/train

# 4. Train
python quick_start_training.py

# 5. Test
python test_trained_model.py --image test.tif

# 6. Compare
python demo_detection.py test.tif

# 7. Deploy
# Update routers/detection.py with your model path
uvicorn main:app --reload
```

---

**🚀 Ready? Start with:**
```bash
python create_sample_dataset.py
```

**Questions? Read:**
- TRAINING_GUIDE.md for detailed instructions
- README_TRAINING.md for full documentation
