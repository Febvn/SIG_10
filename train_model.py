"""
Script untuk training model YOLOv8 dengan data custom untuk deteksi wilayah
Author: Enhanced Training System
"""

import os
from ultralytics import YOLO
import yaml
from pathlib import Path


class ModelTrainer:
    def __init__(self, model_size='n', task='detect'):
        """
        Initialize model trainer
        
        Args:
            model_size: 'n' (nano), 's' (small), 'm' (medium), 'l' (large), 'x' (xlarge)
            task: 'detect' for bounding boxes, 'obb' for oriented bounding boxes
        """
        self.model_size = model_size
        self.task = task
        
        if task == 'obb':
            self.model = YOLO(f'yolov8{model_size}-obb.pt')
        else:
            self.model = YOLO(f'yolov8{model_size}.pt')
    
    def create_dataset_config(self, dataset_path, class_names, output_file='dataset.yaml'):
        """
        Create YAML configuration for dataset
        
        Args:
            dataset_path: Path to dataset folder
            class_names: List of class names (e.g., ['building', 'road', 'tree'])
            output_file: Output YAML filename
        """
        config = {
            'path': str(Path(dataset_path).absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'test': 'images/test',
            'names': {i: name for i, name in enumerate(class_names)}
        }
        
        config_path = os.path.join(dataset_path, output_file)
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print(f"✅ Dataset config created: {config_path}")
        return config_path
    
    def train(
        self,
        data_yaml,
        epochs=100,
        imgsz=640,
        batch=16,
        patience=50,
        save_dir='runs/train',
        device='0',  # '0' for GPU, 'cpu' for CPU
        **kwargs
    ):
        """
        Train the model
        
        Args:
            data_yaml: Path to dataset YAML configuration
            epochs: Number of training epochs
            imgsz: Image size for training
            batch: Batch size
            patience: Early stopping patience
            save_dir: Directory to save training results
            device: Device to use ('0' for GPU, 'cpu' for CPU)
            **kwargs: Additional training arguments
        """
        print("🚀 Starting training...")
        print(f"Model: YOLOv8{self.model_size}-{self.task}")
        print(f"Epochs: {epochs}")
        print(f"Image size: {imgsz}")
        print(f"Batch size: {batch}")
        
        results = self.model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            patience=patience,
            save=True,
            project=save_dir,
            name='exp',
            exist_ok=True,
            pretrained=True,
            optimizer='AdamW',  # AdamW optimizer untuk hasil lebih baik
            lr0=0.01,  # Initial learning rate
            lrf=0.01,  # Final learning rate
            momentum=0.937,
            weight_decay=0.0005,
            warmup_epochs=3,
            warmup_momentum=0.8,
            warmup_bias_lr=0.1,
            box=7.5,  # Box loss gain
            cls=0.5,  # Class loss gain
            dfl=1.5,  # DFL loss gain
            device=device,
            workers=8,
            # Augmentations untuk meningkatkan akurasi
            hsv_h=0.015,  # HSV-Hue augmentation
            hsv_s=0.7,    # HSV-Saturation augmentation
            hsv_v=0.4,    # HSV-Value augmentation
            degrees=0.0,   # Rotation augmentation
            translate=0.1, # Translation augmentation
            scale=0.5,     # Scale augmentation
            shear=0.0,     # Shear augmentation
            perspective=0.0,  # Perspective augmentation
            flipud=0.0,    # Flip up-down
            fliplr=0.5,    # Flip left-right
            mosaic=1.0,    # Mosaic augmentation
            mixup=0.0,     # Mixup augmentation
            copy_paste=0.0, # Copy-paste augmentation
            **kwargs
        )
        
        print("\n✅ Training completed!")
        print(f"Best model saved at: {self.model.trainer.best}")
        
        return results
    
    def validate(self, data_yaml, imgsz=640):
        """Validate the trained model"""
        print("\n📊 Validating model...")
        results = self.model.val(data=data_yaml, imgsz=imgsz)
        return results
    
    def export_model(self, format='onnx', output_path='best_model'):
        """
        Export trained model to different formats
        
        Args:
            format: 'onnx', 'torchscript', 'coreml', 'tflite', etc.
            output_path: Output path for exported model
        """
        print(f"\n📦 Exporting model to {format}...")
        self.model.export(format=format)
        print(f"✅ Model exported successfully!")


def setup_dataset_structure(base_path='dataset'):
    """
    Create proper dataset folder structure for YOLO training
    
    Structure:
    dataset/
    ├── images/
    │   ├── train/
    │   ├── val/
    │   └── test/
    └── labels/
        ├── train/
        ├── val/
        └── test/
    """
    folders = [
        'images/train',
        'images/val', 
        'images/test',
        'labels/train',
        'labels/val',
        'labels/test'
    ]
    
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
    
    print(f"✅ Dataset structure created at: {base_path}")
    print("\n📝 Next steps:")
    print("1. Place your images in images/train, images/val, images/test")
    print("2. Place corresponding label files (.txt) in labels/train, labels/val, labels/test")
    print("3. Label format: <class> <x_center> <y_center> <width> <height> (normalized 0-1)")
    print("\nFor oriented bounding boxes (OBB):")
    print("   Label format: <class> <x1> <y1> <x2> <y2> <x3> <y3> <x4> <y4> (normalized 0-1)")
    
    return base_path


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("🎯 YOLOv8 Model Training Script - Enhanced Version")
    print("=" * 60)
    
    # Setup dataset structure
    dataset_path = setup_dataset_structure('dataset')
    
    # Example: Train a model
    # Uncomment and modify below when you have your dataset ready
    
    """
    # Define your classes
    classes = ['wilayah_pemukiman', 'wilayah_hutan', 'wilayah_pertanian', 'wilayah_industri']
    
    # Initialize trainer with small model for faster training
    # Use 'm' or 'l' for better accuracy but slower training
    trainer = ModelTrainer(model_size='s', task='detect')
    
    # Create dataset config
    config_path = trainer.create_dataset_config(
        dataset_path=dataset_path,
        class_names=classes,
        output_file='dataset.yaml'
    )
    
    # Train the model
    results = trainer.train(
        data_yaml=config_path,
        epochs=100,
        imgsz=640,
        batch=16,
        patience=50,
        device='0'  # Use 'cpu' if no GPU available
    )
    
    # Validate the model
    trainer.validate(data_yaml=config_path)
    
    # Export model (optional)
    # trainer.export_model(format='onnx')
    """
    
    print("\n" + "=" * 60)
    print("📚 Training script ready!")
    print("Modify the example code in __main__ section to start training")
    print("=" * 60)
