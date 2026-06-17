"""
Script untuk testing model yang sudah di-training
"""

import os
import sys
from pathlib import Path
from detection.detector_enhanced import EnhancedSatelliteDetector
import json


def test_model(
    model_path,
    test_image_path,
    output_folder='test_results',
    conf_threshold=0.25
):
    """
    Test trained model pada gambar
    
    Args:
        model_path: Path ke model yang sudah di-training
        test_image_path: Path ke gambar test
        output_folder: Folder untuk menyimpan hasil
        conf_threshold: Confidence threshold
    """
    print("=" * 80)
    print(" 🧪 TESTING TRAINED MODEL ")
    print("=" * 80)
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"\n❌ Model not found: {model_path}")
        print("\n💡 Train a model first using:")
        print("   python quick_start_training.py")
        return
    
    # Check if test image exists
    if not os.path.exists(test_image_path):
        print(f"\n❌ Test image not found: {test_image_path}")
        print("\n💡 Provide a valid image path")
        return
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"\n📦 Loading model: {model_path}")
    detector = EnhancedSatelliteDetector(
        model_path=model_path,
        conf_threshold=conf_threshold,
        iou_threshold=0.45
    )
    
    print(f"🖼️  Processing image: {test_image_path}")
    
    # Generate output paths
    image_name = Path(test_image_path).stem
    vis_output = os.path.join(output_folder, f"{image_name}_detected.jpg")
    json_output = os.path.join(output_folder, f"{image_name}_result.geojson")
    
    # Run detection with visualization
    print(f"🔍 Running detection (conf={conf_threshold})...")
    geojson_result, detections = detector.run_detection(
        image_path=test_image_path,
        visualize=True,
        output_path=vis_output,
        conf=conf_threshold
    )
    
    # Save GeoJSON
    with open(json_output, 'w') as f:
        json.dump(geojson_result, f, indent=2)
    
    # Print results
    print("\n" + "=" * 80)
    print(" ✅ DETECTION COMPLETED ")
    print("=" * 80)
    
    print(f"\n📊 Results:")
    print(f"   Total detections: {len(detections)}")
    
    # Count by class
    class_counts = {}
    for det in detections:
        class_name = det['class_name']
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
    
    print(f"\n📈 Detections by class:")
    for class_name, count in sorted(class_counts.items()):
        print(f"   {class_name}: {count}")
    
    print(f"\n💾 Output files:")
    print(f"   Visualization: {vis_output}")
    print(f"   GeoJSON: {json_output}")
    
    print(f"\n🎯 Average confidence: {sum(d['score'] for d in detections) / len(detections):.3f}" if detections else "   No detections")
    
    return geojson_result, detections


def batch_test(
    model_path,
    test_images_folder,
    output_folder='test_results',
    conf_threshold=0.25
):
    """
    Test model pada banyak gambar sekaligus
    
    Args:
        model_path: Path ke model
        test_images_folder: Folder berisi gambar test
        output_folder: Folder output
        conf_threshold: Confidence threshold
    """
    print("=" * 80)
    print(" 🧪 BATCH TESTING ")
    print("=" * 80)
    
    # Get all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']
    test_images = []
    
    for ext in image_extensions:
        test_images.extend(list(Path(test_images_folder).glob(f'*{ext}')))
        test_images.extend(list(Path(test_images_folder).glob(f'*{ext.upper()}')))
    
    if not test_images:
        print(f"\n❌ No images found in: {test_images_folder}")
        return
    
    print(f"\n📁 Found {len(test_images)} images")
    
    # Create detector
    detector = EnhancedSatelliteDetector(
        model_path=model_path,
        conf_threshold=conf_threshold
    )
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each image
    all_results = []
    total_detections = 0
    
    for idx, image_path in enumerate(test_images, 1):
        print(f"\n[{idx}/{len(test_images)}] Processing: {image_path.name}")
        
        try:
            image_name = image_path.stem
            vis_output = os.path.join(output_folder, f"{image_name}_detected.jpg")
            
            geojson_result, detections = detector.run_detection(
                image_path=str(image_path),
                visualize=True,
                output_path=vis_output,
                conf=conf_threshold
            )
            
            all_results.append({
                'image': image_path.name,
                'detections': len(detections),
                'output': vis_output
            })
            
            total_detections += len(detections)
            print(f"   ✅ Found {len(detections)} objects")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            all_results.append({
                'image': image_path.name,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 80)
    print(" 📊 BATCH TEST SUMMARY ")
    print("=" * 80)
    
    print(f"\n✅ Processed: {len(test_images)} images")
    print(f"🎯 Total detections: {total_detections}")
    print(f"📈 Average per image: {total_detections / len(test_images):.1f}")
    
    # Save summary
    summary_path = os.path.join(output_folder, 'batch_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test trained YOLO model')
    parser.add_argument(
        '--model',
        type=str,
        default='runs/train/exp/weights/best.pt',
        help='Path to trained model'
    )
    parser.add_argument(
        '--image',
        type=str,
        help='Path to single test image'
    )
    parser.add_argument(
        '--folder',
        type=str,
        help='Path to folder with test images (batch mode)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='test_results',
        help='Output folder for results'
    )
    parser.add_argument(
        '--conf',
        type=float,
        default=0.25,
        help='Confidence threshold (0.0-1.0)'
    )
    
    args = parser.parse_args()
    
    if args.folder:
        # Batch testing
        batch_test(
            model_path=args.model,
            test_images_folder=args.folder,
            output_folder=args.output,
            conf_threshold=args.conf
        )
    elif args.image:
        # Single image testing
        test_model(
            model_path=args.model,
            test_image_path=args.image,
            output_folder=args.output,
            conf_threshold=args.conf
        )
    else:
        print("=" * 80)
        print(" 🧪 MODEL TESTING SCRIPT ")
        print("=" * 80)
        
        print("\n📖 Usage:")
        print("\n1. Test single image:")
        print("   python test_trained_model.py --image path/to/image.jpg")
        
        print("\n2. Test multiple images:")
        print("   python test_trained_model.py --folder path/to/images/")
        
        print("\n3. Custom model and confidence:")
        print("   python test_trained_model.py --image test.jpg --model my_model.pt --conf 0.3")
        
        print("\n📝 Parameters:")
        print("   --model   : Path to trained model (default: runs/train/exp/weights/best.pt)")
        print("   --image   : Single image to test")
        print("   --folder  : Folder with multiple images")
        print("   --output  : Output folder (default: test_results)")
        print("   --conf    : Confidence threshold (default: 0.25)")
        
        print("\n💡 Examples:")
        print("   python test_trained_model.py --image lampung.tif")
        print("   python test_trained_model.py --folder data/tif_samples/ --conf 0.3")


if __name__ == "__main__":
    main()
