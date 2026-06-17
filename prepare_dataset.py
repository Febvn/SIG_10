"""
Script untuk mempersiapkan dataset dari citra satelit untuk training YOLO
Includes tools for labeling and data preparation
"""

import os
import cv2
import json
import numpy as np
from pathlib import Path
import shutil
from typing import List, Tuple


class DatasetPreparer:
    """Helper class untuk mempersiapkan dataset YOLO"""
    
    def __init__(self, output_dir='dataset'):
        self.output_dir = Path(output_dir)
        self.setup_directories()
    
    def setup_directories(self):
        """Create dataset directory structure"""
        dirs = [
            'images/train',
            'images/val',
            'images/test',
            'labels/train',
            'labels/val',
            'labels/test',
            'raw_images',
            'temp'
        ]
        
        for d in dirs:
            (self.output_dir / d).mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Directory structure created at: {self.output_dir}")
    
    def split_large_image(
        self,
        image_path: str,
        output_folder: str,
        tile_size: int = 640,
        overlap: int = 100,
        prefix: str = 'tile'
    ) -> List[str]:
        """
        Split large satellite image into smaller tiles for training
        
        Args:
            image_path: Path to large image
            output_folder: Folder to save tiles
            tile_size: Size of each tile
            overlap: Overlap between tiles
            prefix: Prefix for tile filenames
        
        Returns:
            List of tile filenames
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        height, width = img.shape[:2]
        stride = tile_size - overlap
        
        tile_paths = []
        tile_idx = 0
        
        for y in range(0, height - tile_size + 1, stride):
            for x in range(0, width - tile_size + 1, stride):
                tile = img[y:y+tile_size, x:x+tile_size]
                
                tile_filename = f"{prefix}_{tile_idx:04d}.jpg"
                tile_path = os.path.join(output_folder, tile_filename)
                
                cv2.imwrite(tile_path, tile)
                tile_paths.append(tile_filename)
                
                tile_idx += 1
        
        print(f"✅ Created {len(tile_paths)} tiles from {image_path}")
        return tile_paths
    
    def create_yolo_label(
        self,
        image_width: int,
        image_height: int,
        bboxes: List[Tuple],
        output_path: str,
        format: str = 'xyxy'
    ):
        """
        Create YOLO format label file
        
        Args:
            image_width: Image width
            image_height: Image height
            bboxes: List of (class_id, x1, y1, x2, y2) or normalized values
            output_path: Path to save label file
            format: 'xyxy' for pixel coords, 'normalized' if already normalized
        """
        with open(output_path, 'w') as f:
            for bbox in bboxes:
                if format == 'xyxy':
                    class_id, x1, y1, x2, y2 = bbox
                    
                    # Convert to YOLO format (normalized xywh)
                    x_center = ((x1 + x2) / 2) / image_width
                    y_center = ((y1 + y2) / 2) / image_height
                    box_width = (x2 - x1) / image_width
                    box_height = (y2 - y1) / image_height
                else:
                    class_id, x_center, y_center, box_width, box_height = bbox
                
                # Write to file
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")
        
        print(f"✅ Label saved: {output_path}")
    
    def visualize_labels(
        self,
        image_path: str,
        label_path: str,
        class_names: List[str],
        output_path: str = None
    ):
        """
        Visualize YOLO labels on image for verification
        
        Args:
            image_path: Path to image
            label_path: Path to YOLO label file
            class_names: List of class names
            output_path: Path to save visualization (optional)
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Cannot read image: {image_path}")
            return
        
        height, width = img.shape[:2]
        
        # Read labels
        if not os.path.exists(label_path):
            print(f"⚠️ Label file not found: {label_path}")
            return
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ]
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            
            class_id = int(parts[0])
            x_center = float(parts[1]) * width
            y_center = float(parts[2]) * height
            box_width = float(parts[3]) * width
            box_height = float(parts[4]) * height
            
            # Calculate corners
            x1 = int(x_center - box_width / 2)
            y1 = int(y_center - box_height / 2)
            x2 = int(x_center + box_width / 2)
            y2 = int(y_center + box_height / 2)
            
            # Draw rectangle
            color = colors[class_id % len(colors)]
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
            cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        if output_path:
            cv2.imwrite(output_path, img)
            print(f"💾 Visualization saved: {output_path}")
        else:
            cv2.imshow("Labels Visualization", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    def split_dataset(
        self,
        images_folder: str,
        labels_folder: str,
        train_ratio: float = 0.7,
        val_ratio: float = 0.2,
        test_ratio: float = 0.1
    ):
        """
        Split dataset into train/val/test sets
        
        Args:
            images_folder: Folder containing all images
            labels_folder: Folder containing all labels
            train_ratio: Ratio for training set
            val_ratio: Ratio for validation set
            test_ratio: Ratio for test set
        """
        if not np.isclose(train_ratio + val_ratio + test_ratio, 1.0):
            raise ValueError("Ratios must sum to 1.0")
        
        # Get all image files
        image_files = [f for f in os.listdir(images_folder) 
                       if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        # Shuffle
        np.random.shuffle(image_files)
        
        # Calculate splits
        total = len(image_files)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)
        
        train_files = image_files[:train_end]
        val_files = image_files[train_end:val_end]
        test_files = image_files[val_end:]
        
        # Copy files
        for files, split in [(train_files, 'train'), (val_files, 'val'), (test_files, 'test')]:
            for filename in files:
                # Copy image
                src_img = os.path.join(images_folder, filename)
                dst_img = self.output_dir / 'images' / split / filename
                shutil.copy2(src_img, dst_img)
                
                # Copy label
                label_filename = os.path.splitext(filename)[0] + '.txt'
                src_label = os.path.join(labels_folder, label_filename)
                if os.path.exists(src_label):
                    dst_label = self.output_dir / 'labels' / split / label_filename
                    shutil.copy2(src_label, dst_label)
        
        print(f"✅ Dataset split complete:")
        print(f"   Train: {len(train_files)} images")
        print(f"   Val: {len(val_files)} images")
        print(f"   Test: {len(test_files)} images")
    
    def augment_image(self, image_path: str, output_folder: str, num_augmentations: int = 5):
        """
        Apply data augmentation to increase dataset size
        
        Args:
            image_path: Path to input image
            output_folder: Folder to save augmented images
            num_augmentations: Number of augmented versions to create
        """
        img = cv2.imread(image_path)
        if img is None:
            return
        
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        for i in range(num_augmentations):
            aug_img = img.copy()
            
            # Random flip
            if np.random.rand() > 0.5:
                aug_img = cv2.flip(aug_img, 1)  # Horizontal flip
            
            # Random brightness
            brightness = np.random.uniform(0.7, 1.3)
            aug_img = np.clip(aug_img * brightness, 0, 255).astype(np.uint8)
            
            # Random contrast
            alpha = np.random.uniform(0.8, 1.2)
            aug_img = np.clip(alpha * aug_img, 0, 255).astype(np.uint8)
            
            # Save augmented image
            output_path = os.path.join(output_folder, f"{base_name}_aug_{i}.jpg")
            cv2.imwrite(output_path, aug_img)
        
        print(f"✅ Created {num_augmentations} augmentations for {image_path}")


def create_example_labels():
    """Create example label files for demonstration"""
    print("\n" + "="*60)
    print("📝 YOLO Label Format Examples")
    print("="*60)
    
    print("\nFor standard bounding boxes:")
    print("Format: <class_id> <x_center> <y_center> <width> <height>")
    print("All values normalized to 0-1")
    print("\nExample:")
    print("0 0.5 0.5 0.3 0.4")
    print("1 0.2 0.3 0.15 0.2")
    
    print("\nFor oriented bounding boxes (OBB):")
    print("Format: <class_id> <x1> <y1> <x2> <y2> <x3> <y3> <x4> <y4>")
    print("All coordinates normalized to 0-1")
    print("\nExample:")
    print("0 0.1 0.1 0.4 0.1 0.4 0.4 0.1 0.4")


if __name__ == "__main__":
    print("="*60)
    print("🎯 Dataset Preparation Tool for YOLO Training")
    print("="*60)
    
    # Initialize preparer
    preparer = DatasetPreparer(output_dir='dataset')
    
    # Show example label formats
    create_example_labels()
    
    print("\n" + "="*60)
    print("📚 Dataset preparation tools ready!")
    print("="*60)
    
    print("\n💡 Usage Examples:")
    print("\n1. Split large image into tiles:")
    print("   preparer.split_large_image('large_satellite.jpg', 'dataset/temp')")
    
    print("\n2. Create YOLO labels:")
    print("   bboxes = [(0, 100, 100, 200, 200), (1, 300, 300, 400, 400)]")
    print("   preparer.create_yolo_label(640, 640, bboxes, 'labels/image.txt')")
    
    print("\n3. Visualize labels:")
    print("   preparer.visualize_labels('image.jpg', 'labels/image.txt', ['class1', 'class2'])")
    
    print("\n4. Split into train/val/test:")
    print("   preparer.split_dataset('all_images/', 'all_labels/')")
    
    print("\n5. Augment dataset:")
    print("   preparer.augment_image('image.jpg', 'augmented/', num_augmentations=5)")
