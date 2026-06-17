"""
Quick Start Script untuk Training Model YOLO
Jalankan script ini untuk mulai training dengan cepat
"""

import os
from pathlib import Path
from train_model import ModelTrainer, setup_dataset_structure
from prepare_dataset import DatasetPreparer

def main():
    print("=" * 80)
    print(" 🚀 QUICK START - YOLO MODEL TRAINING ")
    print("=" * 80)
    
    # Step 1: Setup Dataset
    print("\n📁 Step 1: Setting up dataset structure...")
    dataset_path = setup_dataset_structure('dataset')
    
    # Step 2: Check if dataset has images
    train_images = list(Path('dataset/images/train').glob('*.jpg')) + \
                   list(Path('dataset/images/train').glob('*.png'))
    
    if len(train_images) == 0:
        print("\n⚠️  WARNING: No training images found!")
        print("\n📝 To continue, you need to:")
        print("   1. Add images to: dataset/images/train/")
        print("   2. Add labels to: dataset/labels/train/")
        print("   3. Add images to: dataset/images/val/")
        print("   4. Add labels to: dataset/labels/val/")
        print("\n💡 Use one of these tools to label your data:")
        print("   - LabelImg: https://github.com/HumanSignal/labelImg")
        print("   - Roboflow: https://roboflow.com/")
        print("   - CVAT: https://www.cvat.ai/")
        print("\n📖 Read TRAINING_GUIDE.md for detailed instructions")
        return
    
    print(f"✅ Found {len(train_images)} training images")
    
    # Step 3: Define your classes
    print("\n🏷️  Step 2: Define your classes...")
    print("\n💡 Edit this list to match your object classes:")
    
    classes = [
        'wilayah_pemukiman',
        'wilayah_hutan',
        'wilayah_pertanian',
        'wilayah_industri',
        'wilayah_pesisir'
    ]
    
    print(f"   Classes: {', '.join(classes)}")
    
    # Step 4: Choose model size
    print("\n🤖 Step 3: Choose model size...")
    print("\n   Available models:")
    print("   - 'n' (nano)   : Fastest, good for testing")
    print("   - 's' (small)  : Fast, balanced (RECOMMENDED)")
    print("   - 'm' (medium) : Good accuracy")
    print("   - 'l' (large)  : High accuracy")
    print("   - 'x' (xlarge) : Best accuracy, slowest")
    
    model_size = 's'  # Change this if needed
    print(f"\n   Selected: YOLOv8{model_size}")
    
    # Step 5: Training parameters
    print("\n⚙️  Step 4: Training configuration...")
    
    config = {
        'epochs': 100,
        'imgsz': 640,
        'batch': 16,
        'device': '0',  # Change to 'cpu' if no GPU
        'patience': 50
    }
    
    print(f"   Epochs: {config['epochs']}")
    print(f"   Image size: {config['imgsz']}")
    print(f"   Batch size: {config['batch']}")
    print(f"   Device: {config['device']} (GPU)" if config['device'] != 'cpu' else f"   Device: CPU")
    print(f"   Early stopping patience: {config['patience']}")
    
    # Step 6: Confirm before training
    print("\n" + "=" * 80)
    print("🎯 Ready to start training!")
    print("=" * 80)
    
    response = input("\n⚠️  Start training now? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("\n❌ Training cancelled.")
        print("💡 Modify this script or use train_model.py directly for custom training")
        return
    
    # Step 7: Initialize trainer
    print("\n🚀 Initializing trainer...")
    trainer = ModelTrainer(model_size=model_size, task='detect')
    
    # Step 8: Create dataset config
    print("\n📝 Creating dataset configuration...")
    config_path = trainer.create_dataset_config(
        dataset_path=dataset_path,
        class_names=classes,
        output_file='dataset.yaml'
    )
    
    # Step 9: Start training
    print("\n🏋️  Starting training...")
    print("   This may take a while depending on your dataset size and hardware...")
    print("   Monitor the progress in the terminal\n")
    
    try:
        results = trainer.train(
            data_yaml=config_path,
            epochs=config['epochs'],
            imgsz=config['imgsz'],
            batch=config['batch'],
            patience=config['patience'],
            device=config['device'],
            save_dir='runs/train'
        )
        
        print("\n" + "=" * 80)
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        print(f"\n📁 Results saved to: runs/train/exp/")
        print(f"🏆 Best model: runs/train/exp/weights/best.pt")
        print(f"📊 Metrics: runs/train/exp/results.csv")
        print(f"📈 Plots: runs/train/exp/")
        
        # Step 10: Validate
        print("\n📊 Running validation...")
        val_results = trainer.validate(data_yaml=config_path)
        
        print(f"\n🎯 Validation Results:")
        print(f"   mAP50: {val_results.box.map50:.4f}")
        print(f"   mAP50-95: {val_results.box.map:.4f}")
        
        # Step 11: Next steps
        print("\n" + "=" * 80)
        print("🎉 NEXT STEPS")
        print("=" * 80)
        
        print("\n1. Test your model:")
        print("   python test_trained_model.py")
        
        print("\n2. Use in API:")
        print("   Update model_path in detection/detector_enhanced.py")
        print("   detector = EnhancedSatelliteDetector(")
        print("       model_path='runs/train/exp/weights/best.pt'")
        print("   )")
        
        print("\n3. Export model:")
        print("   trainer.export_model(format='onnx')")
        
        print("\n4. Improve accuracy:")
        print("   - Add more training data")
        print("   - Try larger model (YOLOv8m or YOLOv8l)")
        print("   - Increase epochs")
        print("   - Read TRAINING_GUIDE.md for more tips")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
        print("💾 Partial results saved in runs/train/exp/")
        
    except Exception as e:
        print(f"\n\n❌ Error during training: {str(e)}")
        print("\n🐛 Troubleshooting:")
        print("   - Check dataset structure is correct")
        print("   - Verify labels are in correct YOLO format")
        print("   - Try reducing batch size if CUDA out of memory")
        print("   - Read TRAINING_GUIDE.md for help")


if __name__ == "__main__":
    main()
