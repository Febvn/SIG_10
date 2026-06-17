"""
Script untuk membuat sample dataset dari GeoTIFF files
Otomatis split menjadi tiles dan siap untuk labeling
"""

import os
import cv2
import numpy as np
from pathlib import Path
from prepare_dataset import DatasetPreparer
import json


def create_sample_dataset_from_tif(
    tif_folder='data/tif_samples',
    output_folder='dataset',
    tile_size=640,
    overlap=100,
    sample_limit=None
):
    """
    Buat sample dataset dari GeoTIFF files
    
    Args:
        tif_folder: Folder berisi file TIF
        output_folder: Output folder untuk dataset
        tile_size: Ukuran tile
        overlap: Overlap antar tile
        sample_limit: Limit jumlah tile per image (None = all)
    """
    print("=" * 80)
    print(" 📦 CREATING SAMPLE DATASET FROM GEOTIFF ")
    print("=" * 80)
    
    # Check if tif folder exists
    if not os.path.exists(tif_folder):
        print(f"\n❌ TIF folder not found: {tif_folder}")
        print("\n💡 Available options:")
        print("   1. Create 'data/tif_samples' folder")
        print("   2. Place your GeoTIFF files there")
        print("   3. Run this script again")
        return
    
    # Find all TIF files
    tif_files = []
    for ext in ['.tif', '.tiff', '.TIF', '.TIFF']:
        tif_files.extend(list(Path(tif_folder).glob(f'*{ext}')))
    
    if not tif_files:
        print(f"\n❌ No TIF files found in: {tif_folder}")
        return
    
    print(f"\n✅ Found {len(tif_files)} TIF files")
    
    # Initialize preparer
    preparer = DatasetPreparer(output_dir=output_folder)
    
    # Create temp folder for tiles
    temp_folder = os.path.join(output_folder, 'temp')
    os.makedirs(temp_folder, exist_ok=True)
    
    # Process each TIF file
    all_tiles = []
    tile_metadata = []
    
    for idx, tif_path in enumerate(tif_files, 1):
        print(f"\n[{idx}/{len(tif_files)}] Processing: {tif_path.name}")
        
        try:
            # Split into tiles
            tiles = preparer.split_large_image(
                image_path=str(tif_path),
                output_folder=temp_folder,
                tile_size=tile_size,
                overlap=overlap,
                prefix=tif_path.stem
            )
            
            # Limit samples if specified
            if sample_limit and len(tiles) > sample_limit:
                import random
                tiles = random.sample(tiles, sample_limit)
                print(f"   ℹ️  Limited to {sample_limit} tiles")
            
            all_tiles.extend(tiles)
            
            # Save metadata
            tile_metadata.append({
                'source': str(tif_path),
                'tiles_generated': len(tiles),
                'tile_size': tile_size,
                'overlap': overlap
            })
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n✅ Total tiles created: {len(all_tiles)}")
    
    # Split into train/val/test (but only copy images, labels need to be created)
    print("\n📂 Organizing into train/val/test folders...")
    
    import random
    random.shuffle(all_tiles)
    
    train_split = int(len(all_tiles) * 0.7)
    val_split = int(len(all_tiles) * 0.2)
    
    train_tiles = all_tiles[:train_split]
    val_tiles = all_tiles[train_split:train_split + val_split]
    test_tiles = all_tiles[train_split + val_split:]
    
    # Copy tiles to respective folders
    import shutil
    
    for tiles, split in [(train_tiles, 'train'), (val_tiles, 'val'), (test_tiles, 'test')]:
        for tile_name in tiles:
            src = os.path.join(temp_folder, tile_name)
            dst = os.path.join(output_folder, 'images', split, tile_name)
            
            if os.path.exists(src):
                shutil.copy2(src, dst)
                
                # Create empty label file as placeholder
                label_name = os.path.splitext(tile_name)[0] + '.txt'
                label_path = os.path.join(output_folder, 'labels', split, label_name)
                
                # Create empty file (you'll fill this during labeling)
                with open(label_path, 'w') as f:
                    pass
    
    # Save metadata
    metadata_path = os.path.join(output_folder, 'dataset_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump({
            'total_tiles': len(all_tiles),
            'train': len(train_tiles),
            'val': len(val_tiles),
            'test': len(test_tiles),
            'tile_size': tile_size,
            'overlap': overlap,
            'source_files': tile_metadata
        }, f, indent=2)
    
    print(f"\n📊 Dataset split:")
    print(f"   Train: {len(train_tiles)} images")
    print(f"   Val:   {len(val_tiles)} images")
    print(f"   Test:  {len(test_tiles)} images")
    
    print(f"\n💾 Metadata saved: {metadata_path}")
    
    # Create example classes file
    example_classes_path = os.path.join(output_folder, 'classes_example.txt')
    with open(example_classes_path, 'w') as f:
        f.write("# Define your classes here (one per line)\n")
        f.write("# Example for land use detection:\n")
        f.write("wilayah_pemukiman\n")
        f.write("wilayah_hutan\n")
        f.write("wilayah_pertanian\n")
        f.write("wilayah_industri\n")
        f.write("wilayah_pesisir\n")
    
    print(f"\n📝 Example classes file: {example_classes_path}")
    
    # Instructions
    print("\n" + "=" * 80)
    print(" 🎯 NEXT STEPS ")
    print("=" * 80)
    
    print("\n1️⃣  LABEL YOUR DATA:")
    print("   Use one of these tools:")
    print("   • LabelImg: https://github.com/HumanSignal/labelImg")
    print("   • Roboflow: https://roboflow.com/")
    print("   • CVAT: https://www.cvat.ai/")
    
    print("\n2️⃣  DEFINE YOUR CLASSES:")
    print(f"   Edit: {example_classes_path}")
    print("   Remove example classes and add your own")
    
    print("\n3️⃣  START LABELING:")
    print(f"   Label images in: {output_folder}/images/train/")
    print(f"   Save labels to: {output_folder}/labels/train/")
    
    print("\n4️⃣  LABEL FORMAT:")
    print("   YOLO format: <class_id> <x_center> <y_center> <width> <height>")
    print("   All values normalized (0.0 - 1.0)")
    print("   Example: 0 0.5 0.5 0.3 0.4")
    
    print("\n5️⃣  VERIFY LABELS:")
    print("   python -c \"")
    print("   from prepare_dataset import DatasetPreparer")
    print("   p = DatasetPreparer()")
    print("   p.visualize_labels('dataset/images/train/image.jpg',")
    print("                      'dataset/labels/train/image.txt',")
    print("                      ['class1', 'class2'])\"")
    
    print("\n6️⃣  START TRAINING:")
    print("   python quick_start_training.py")
    
    print("\n💡 Tips:")
    print("   • Start with train set only")
    print("   • Label at least 50-100 images per class")
    print("   • Be consistent with your labels")
    print("   • Validate labels with visualization before training")
    
    return output_folder


def visualize_sample_tiles(dataset_folder='dataset', num_samples=5):
    """
    Visualize beberapa sample tiles
    
    Args:
        dataset_folder: Dataset folder
        num_samples: Jumlah sample yang ditampilkan
    """
    print("\n📸 Visualizing sample tiles...")
    
    train_folder = os.path.join(dataset_folder, 'images', 'train')
    
    if not os.path.exists(train_folder):
        print(f"   ⚠️  Train folder not found: {train_folder}")
        return
    
    # Get sample images
    images = list(Path(train_folder).glob('*.jpg'))[:num_samples]
    
    if not images:
        print(f"   ⚠️  No images found in: {train_folder}")
        return
    
    # Create visualization
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, len(images), figsize=(15, 3))
    
    if len(images) == 1:
        axes = [axes]
    
    for ax, img_path in zip(axes, images):
        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        ax.imshow(img)
        ax.set_title(img_path.name, fontsize=8)
        ax.axis('off')
    
    plt.tight_layout()
    
    output_path = os.path.join(dataset_folder, 'sample_tiles_preview.jpg')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Sample preview saved: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Create sample dataset from GeoTIFF files')
    parser.add_argument(
        '--input',
        type=str,
        default='data/tif_samples',
        help='Input folder with TIF files'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='dataset',
        help='Output dataset folder'
    )
    parser.add_argument(
        '--tile-size',
        type=int,
        default=640,
        help='Tile size in pixels'
    )
    parser.add_argument(
        '--overlap',
        type=int,
        default=100,
        help='Overlap between tiles in pixels'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit tiles per image (optional)'
    )
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Create visualization of sample tiles'
    )
    
    args = parser.parse_args()
    
    # Create dataset
    dataset_folder = create_sample_dataset_from_tif(
        tif_folder=args.input,
        output_folder=args.output,
        tile_size=args.tile_size,
        overlap=args.overlap,
        sample_limit=args.limit
    )
    
    # Visualize if requested
    if args.visualize and dataset_folder:
        visualize_sample_tiles(dataset_folder)
    
    print("\n" + "=" * 80)
    print(" ✅ DATASET CREATION COMPLETED ")
    print("=" * 80)


if __name__ == "__main__":
    main()
