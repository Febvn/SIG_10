# ⚡ Cheat Sheet - Quick Reference

Referensi cepat untuk semua command dan workflow.

---

## 🚀 Quick Commands

### Setup & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Download model (auto on first run)
# Models: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
```

### Dataset Preparation
```bash
# Create dataset from GeoTIFF
python create_sample_dataset.py

# With custom parameters
python create_sample_dataset.py \
    --input data/tif_samples \
    --output dataset \
    --tile-size 640 \
    --overlap 100 \
    --limit 500

# Install LabelImg for labeling
pip install labelImg
labelImg dataset/images/train
```

### Training
```bash
# Quick start (interactive)
python quick_start_training.py

# Custom training (edit script first)
python train_model.py
```

### Testing
```bash
# Test single image
python test_trained_model.py --image test.tif

# Test multiple images
python test_trained_model.py --folder data/tif_samples/

# With custom parameters
python test_trained_model.py \
    --image test.tif \
    --model runs/train/exp/weights/best.pt \
    --conf 0.3 \
    --output results/

# Compare before/after
python demo_detection.py test.tif
```

### API Server
```bash
# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test endpoint (standard)
curl -X POST "http://localhost:8000/detection/process" \
  -F "file=@test.tif"

# Test endpoint (enhanced with visualization)
curl -X POST "http://localhost:8000/detection/process?use_enhanced=true&visualize=true&conf_threshold=0.25" \
  -F "file=@test.tif"

# Get classes
curl "http://localhost:8000/detection/classes"
```

---

## 💻 Code Snippets

### Training Model
```python
from train_model import ModelTrainer

# Initialize
trainer = ModelTrainer(model_size='s', task='detect')

# Create config
config_path = trainer.create_dataset_config(
    dataset_path='dataset',
    class_names=['class1', 'class2', 'class3']
)

# Train
results = trainer.train(
    data_yaml=config_path,
    epochs=100,
    batch=16,
    device='0'  # or 'cpu'
)

# Validate
trainer.validate(data_yaml=config_path)
```

### Enhanced Detection
```python
from detection.detector_enhanced import EnhancedSatelliteDetector

# Initialize
detector = EnhancedSatelliteDetector(
    model_path='runs/train/exp/weights/best.pt',
    conf_threshold=0.25,
    iou_threshold=0.45
)

# Detect with visualization
geojson, detections = detector.run_detection(
    image_path='test.tif',
    visualize=True,
    output_path='result.jpg',
    conf=0.25
)

print(f"Found {len(detections)} objects")
```

### Dataset Preparation
```python
from prepare_dataset import DatasetPreparer

preparer = DatasetPreparer()

# Split large image
preparer.split_large_image(
    image_path='large.tif',
    output_folder='dataset/temp',
    tile_size=640,
    overlap=100
)

# Split dataset
preparer.split_dataset(
    images_folder='dataset/temp',
    labels_folder='dataset/temp_labels',
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1
)

# Visualize labels
preparer.visualize_labels(
    image_path='image.jpg',
    label_path='label.txt',
    class_names=['class1', 'class2'],
    output_path='verification.jpg'
)
```

---

## 📊 Model Sizes

| Model | Size | Speed | mAP50 | Use Case |
|-------|------|-------|-------|----------|
| YOLOv8n | 6 MB | ⚡⚡⚡⚡⚡ | ~37% | Testing |
| YOLOv8s | 22 MB | ⚡⚡⚡⚡ | ~45% | Production |
| YOLOv8m | 52 MB | ⚡⚡⚡ | ~50% | High Accuracy |
| YOLOv8l | 87 MB | ⚡⚡ | ~53% | Maximum Accuracy |
| YOLOv8x | 136 MB | ⚡ | ~54% | Research |

---

## 🎯 Training Parameters

### Basic
```python
trainer.train(
    data_yaml='dataset.yaml',
    epochs=100,          # Number of epochs
    imgsz=640,          # Image size
    batch=16,           # Batch size
    device='0',         # '0' for GPU, 'cpu' for CPU
    patience=50         # Early stopping
)
```

### Advanced
```python
trainer.train(
    # Basic
    epochs=200,
    batch=16,
    imgsz=640,
    
    # Optimizer
    optimizer='AdamW',
    lr0=0.01,           # Initial learning rate
    lrf=0.01,           # Final learning rate
    momentum=0.937,
    weight_decay=0.0005,
    
    # Augmentation
    hsv_h=0.015,        # HSV-Hue
    hsv_s=0.7,          # HSV-Saturation
    hsv_v=0.4,          # HSV-Value
    degrees=10.0,       # Rotation
    translate=0.1,      # Translation
    scale=0.5,          # Scale
    shear=2.0,          # Shear
    perspective=0.0,    # Perspective
    flipud=0.0,         # Flip up-down
    fliplr=0.5,         # Flip left-right
    mosaic=1.0,         # Mosaic augmentation
    mixup=0.1           # Mixup augmentation
)
```

---

## 📝 YOLO Label Format

### Standard Bounding Box
```
<class_id> <x_center> <y_center> <width> <height>
```

Example:
```
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.15 0.2
```

All values normalized (0.0 - 1.0)

### Oriented Bounding Box (OBB)
```
<class_id> <x1> <y1> <x2> <y2> <x3> <y3> <x4> <y4>
```

Example:
```
0 0.1 0.1 0.4 0.1 0.4 0.4 0.1 0.4
```

---

## 🗂️ Dataset Structure

```
dataset/
├── images/
│   ├── train/          # Training images (70%)
│   ├── val/            # Validation images (20%)
│   └── test/           # Test images (10%)
└── labels/
    ├── train/          # Training labels
    ├── val/            # Validation labels
    └── test/           # Test labels
```

---

## 🔧 Common Fixes

### CUDA Out of Memory
```python
# Reduce batch size
trainer.train(batch=8)  # or 4, 2
```

### No Detections
```python
# Lower confidence threshold
detector.run_detection(conf=0.1)

# Or check model path
detector = EnhancedSatelliteDetector(
    model_path='runs/train/exp/weights/best.pt'
)
```

### Poor Accuracy
1. Add more training data
2. Use larger model (YOLOv8m or YOLOv8l)
3. Increase epochs
4. Improve label quality
5. Add more augmentation

### Training Too Slow
1. Use smaller model (YOLOv8n)
2. Reduce image size (imgsz=320)
3. Use GPU instead of CPU
4. Reduce batch size if needed

---

## 📈 Metrics Interpretation

### mAP (Mean Average Precision)
- **mAP50**: Average precision at IoU=0.5
- **mAP50-95**: Average across IoU 0.5-0.95
- **Target**: mAP50 > 0.5 (50%)

### Training Curves
- **Box Loss**: Should decrease (object localization)
- **Class Loss**: Should decrease (classification)
- **DFL Loss**: Should decrease (distribution focal loss)

### Validation
- **Precision**: How many predictions are correct
- **Recall**: How many objects are detected
- **F1-Score**: Harmonic mean of precision and recall

---

## 🎨 Visualization Colors

Default color palette (BGR):
```python
colors = [
    (255, 0, 0),     # Blue
    (0, 255, 0),     # Green
    (0, 0, 255),     # Red
    (255, 255, 0),   # Cyan
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Yellow
    (128, 0, 128),   # Purple
    (255, 165, 0),   # Orange
]
```

---

## 📁 Important Paths

```bash
# Dataset
dataset/images/train/          # Training images
dataset/labels/train/          # Training labels

# Models
yolov8n.pt                     # Pre-trained model
runs/train/exp/weights/best.pt # Trained model

# Results
runs/train/exp/                # Training results
test_results/                  # Test outputs
```

---

## 🌐 API Endpoints

### POST /detection/process
**Standard:**
```bash
curl -X POST "http://localhost:8000/detection/process" \
  -F "file=@image.tif"
```

**Enhanced:**
```bash
curl -X POST "http://localhost:8000/detection/process?use_enhanced=true&visualize=true" \
  -F "file=@image.tif"
```

**Parameters:**
- `use_enhanced`: bool (default: false)
- `conf_threshold`: float (default: 0.25)
- `visualize`: bool (default: false)

**Response:**
```json
{
  "geojson": {...},
  "detections_count": 45,
  "visualization": "base64...",
  "visualization_format": "base64_jpeg"
}
```

### GET /detection/classes
```bash
curl "http://localhost:8000/detection/classes"
```

**Response:**
```json
{
  "0": "class1",
  "1": "class2",
  ...
}
```

---

## ⏱️ Time Estimates

### Dataset Preparation
- 100 images: ~5 minutes
- 500 images: ~20 minutes
- 1000 images: ~40 minutes

### Labeling (per image)
- Simple: 1-2 minutes
- Complex: 5-10 minutes

### Training (100 epochs, 500 images)
- YOLOv8n + GPU: 30-60 min
- YOLOv8s + GPU: 1-2 hours
- YOLOv8m + GPU: 2-4 hours
- CPU: 5-10x slower

### Inference (per image)
- YOLOv8n: 10-20ms
- YOLOv8s: 20-30ms
- YOLOv8m: 40-60ms

---

## 🎓 Learning Resources

### Documentation
- QUICKSTART.md - Quick start guide
- TRAINING_GUIDE.md - Complete tutorial
- README_TRAINING.md - System docs
- INDEX.md - File navigation

### External Links
- YOLOv8: https://docs.ultralytics.com/
- Roboflow: https://roboflow.com/
- LabelImg: https://github.com/HumanSignal/labelImg

---

## 🔥 Pro Tips

1. **Start small**: Use YOLOv8n for quick iterations
2. **Verify labels**: Always visualize before training
3. **Balance dataset**: Equal samples per class
4. **Use augmentation**: Increases effective dataset size
5. **Monitor training**: Watch for overfitting
6. **Test early**: Test model after 50 epochs
7. **Fine-tune**: Adjust learning rate if needed
8. **Save checkpoints**: Don't lose progress
9. **Use GPU**: 5-10x faster than CPU
10. **Read docs**: TRAINING_GUIDE.md has all details

---

**Print this page for quick reference! 📄**
