"""
Demo script untuk membandingkan deteksi sebelum dan sesudah training
"""

import os
from detection.detector_enhanced import EnhancedSatelliteDetector
import cv2
import numpy as np


def compare_models(
    image_path,
    pretrained_model='yolov8n-obb.pt',
    trained_model='runs/train/exp/weights/best.pt',
    output_folder='comparison_results'
):
    """
    Bandingkan hasil deteksi antara model pre-trained dan model hasil training
    
    Args:
        image_path: Path ke gambar test
        pretrained_model: Model pre-trained (default YOLO)
        trained_model: Model hasil training custom
        output_folder: Folder output
    """
    print("=" * 80)
    print(" 🔬 MODEL COMPARISON DEMO ")
    print("=" * 80)
    
    if not os.path.exists(image_path):
        print(f"\n❌ Image not found: {image_path}")
        return
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Test with pre-trained model
    print("\n📦 Testing with PRE-TRAINED model...")
    print(f"   Model: {pretrained_model}")
    
    detector_pretrained = EnhancedSatelliteDetector(
        model_path=pretrained_model,
        conf_threshold=0.25
    )
    
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_pretrained = os.path.join(output_folder, f"{image_name}_pretrained.jpg")
    
    try:
        geojson_pre, detections_pre = detector_pretrained.run_detection(
            image_path=image_path,
            visualize=True,
            output_path=output_pretrained,
            conf=0.25
        )
        
        print(f"   ✅ Detections: {len(detections_pre)}")
        
        if len(detections_pre) > 0:
            class_counts_pre = {}
            for det in detections_pre:
                class_name = det['class_name']
                class_counts_pre[class_name] = class_counts_pre.get(class_name, 0) + 1
            
            print("   Classes detected:")
            for cls, count in class_counts_pre.items():
                print(f"      - {cls}: {count}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        detections_pre = []
    
    # Test with trained model (if exists)
    if os.path.exists(trained_model):
        print(f"\n🎯 Testing with TRAINED model...")
        print(f"   Model: {trained_model}")
        
        detector_trained = EnhancedSatelliteDetector(
            model_path=trained_model,
            conf_threshold=0.25
        )
        
        output_trained = os.path.join(output_folder, f"{image_name}_trained.jpg")
        
        try:
            geojson_trained, detections_trained = detector_trained.run_detection(
                image_path=image_path,
                visualize=True,
                output_path=output_trained,
                conf=0.25
            )
            
            print(f"   ✅ Detections: {len(detections_trained)}")
            
            if len(detections_trained) > 0:
                class_counts_trained = {}
                for det in detections_trained:
                    class_name = det['class_name']
                    class_counts_trained[class_name] = class_counts_trained.get(class_name, 0) + 1
                
                print("   Classes detected:")
                for cls, count in class_counts_trained.items():
                    print(f"      - {cls}: {count}")
            
            # Create side-by-side comparison
            print("\n📊 Creating side-by-side comparison...")
            create_comparison_image(
                output_pretrained,
                output_trained,
                os.path.join(output_folder, f"{image_name}_comparison.jpg")
            )
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            detections_trained = []
    else:
        print(f"\n⚠️  Trained model not found: {trained_model}")
        print("   Train a model first using: python quick_start_training.py")
        detections_trained = []
    
    # Summary
    print("\n" + "=" * 80)
    print(" 📊 COMPARISON SUMMARY ")
    print("=" * 80)
    
    print(f"\n📈 Results:")
    print(f"   Pre-trained model: {len(detections_pre)} detections")
    
    if os.path.exists(trained_model):
        print(f"   Trained model:     {len(detections_trained)} detections")
        
        if len(detections_trained) > len(detections_pre):
            improvement = len(detections_trained) - len(detections_pre)
            print(f"\n✅ Improvement: +{improvement} more detections ({improvement / max(len(detections_pre), 1) * 100:.1f}% increase)")
        elif len(detections_trained) < len(detections_pre):
            print(f"\n⚠️  Note: Trained model has fewer detections")
            print(f"   This might be expected if trained for specific classes only")
    
    print(f"\n💾 Output files:")
    print(f"   Pre-trained result: {output_pretrained}")
    if os.path.exists(trained_model):
        print(f"   Trained result:     {output_trained}")
        print(f"   Side-by-side:       {os.path.join(output_folder, f'{image_name}_comparison.jpg')}")


def create_comparison_image(img1_path, img2_path, output_path):
    """Create side-by-side comparison of two images"""
    try:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        
        if img1 is None or img2 is None:
            print("   ⚠️  Could not create comparison (images not found)")
            return
        
        # Resize if needed to match heights
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        target_height = min(h1, h2, 1000)  # Max 1000px height
        
        scale1 = target_height / h1
        scale2 = target_height / h2
        
        img1_resized = cv2.resize(img1, (int(w1 * scale1), target_height))
        img2_resized = cv2.resize(img2, (int(w2 * scale2), target_height))
        
        # Add labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img1_resized, "PRE-TRAINED MODEL", (20, 40), font, 1, (0, 255, 0), 2)
        cv2.putText(img2_resized, "TRAINED MODEL", (20, 40), font, 1, (0, 255, 0), 2)
        
        # Concatenate horizontally
        comparison = np.hstack([img1_resized, img2_resized])
        
        # Add separator line
        h, w = comparison.shape[:2]
        mid = img1_resized.shape[1]
        cv2.line(comparison, (mid, 0), (mid, h), (255, 255, 255), 3)
        
        cv2.imwrite(output_path, comparison)
        print(f"   ✅ Comparison saved: {output_path}")
        
    except Exception as e:
        print(f"   ❌ Error creating comparison: {str(e)}")


def demo_with_sample_images():
    """Run demo on sample images if available"""
    print("=" * 80)
    print(" 🎬 RUNNING DEMO WITH SAMPLE IMAGES ")
    print("=" * 80)
    
    # Look for sample images
    sample_folders = ['data/tif_samples', 'data', '.']
    sample_extensions = ['.tif', '.tiff', '.jpg', '.jpeg', '.png']
    
    sample_images = []
    for folder in sample_folders:
        if os.path.exists(folder):
            for ext in sample_extensions:
                import glob
                pattern = os.path.join(folder, f'*{ext}')
                sample_images.extend(glob.glob(pattern))
                pattern_upper = os.path.join(folder, f'*{ext.upper()}')
                sample_images.extend(glob.glob(pattern_upper))
    
    if not sample_images:
        print("\n⚠️  No sample images found")
        print("\n💡 Usage:")
        print("   python demo_detection.py path/to/your/image.tif")
        return
    
    # Use first sample image
    sample_image = sample_images[0]
    print(f"\n✅ Found sample image: {sample_image}")
    print(f"   Total samples available: {len(sample_images)}")
    
    compare_models(
        image_path=sample_image,
        output_folder='demo_results'
    )


def main():
    import sys
    
    if len(sys.argv) > 1:
        # Image path provided as argument
        image_path = sys.argv[1]
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return
        
        compare_models(image_path=image_path)
    else:
        # Try to find sample images
        demo_with_sample_images()
    
    print("\n" + "=" * 80)
    print(" 🎯 DEMO COMPLETED ")
    print("=" * 80)
    
    print("\n💡 Next steps:")
    print("   1. Review the comparison images in demo_results/ or comparison_results/")
    print("   2. If no trained model exists, run: python quick_start_training.py")
    print("   3. After training, run this demo again to see improvements")
    print("   4. Adjust confidence threshold if needed")


if __name__ == "__main__":
    main()
