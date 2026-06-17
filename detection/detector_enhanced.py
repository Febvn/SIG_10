"""
Enhanced Detector with Visualization and Better Detection
"""

import os
import cv2
import numpy as np
import rasterio
import geojson
from ultralytics import YOLO
from typing import List, Tuple, Dict, Optional
import warnings


def setup_rasterio_env():
    """Fix PROJ_LIB/GDAL_DATA conflicts on Windows."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    venv_base = os.path.dirname(current_dir)
    proj_data = os.path.join(venv_base, ".venv", "Lib", "site-packages", "rasterio", "proj_data")
    gdal_data = os.path.join(venv_base, ".venv", "Lib", "site-packages", "rasterio", "gdal_data")

    if os.path.exists(proj_data):
        os.environ['PROJ_LIB'] = proj_data
    if os.path.exists(gdal_data):
        os.environ['GDAL_DATA'] = gdal_data


setup_rasterio_env()


class EnhancedSatelliteDetector:
    """
    Enhanced detector with visualization capabilities and better detection accuracy
    """
    
    def __init__(self, model_path='yolov8n-obb.pt', conf_threshold=0.25, iou_threshold=0.45):
        """
        Initialize enhanced detector
        
        Args:
            model_path: Path to YOLO model
            conf_threshold: Confidence threshold for detections
            iou_threshold: IOU threshold for NMS
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # Color palette for different classes (BGR format)
        self.colors = [
            (255, 0, 0),     # Blue
            (0, 255, 0),     # Green
            (0, 0, 255),     # Red
            (255, 255, 0),   # Cyan
            (255, 0, 255),   # Magenta
            (0, 255, 255),   # Yellow
            (128, 0, 128),   # Purple
            (255, 165, 0),   # Orange
            (0, 128, 128),   # Teal
            (128, 128, 0),   # Olive
        ]

    def get_tiles(self, img_height, img_width, tile_size=640, overlap=0.2):
        """
        Generate tiles with overlap for better edge detection
        
        Args:
            img_height: Image height
            img_width: Image width
            tile_size: Size of each tile
            overlap: Overlap ratio (0.2 = 20% overlap)
        """
        stride = int(tile_size * (1 - overlap))
        tiles = []
        
        for y in range(0, img_height, stride):
            for x in range(0, img_width, stride):
                y1 = min(y, img_height - tile_size) if y + tile_size > img_height else y
                x1 = min(x, img_width - tile_size) if x + tile_size > img_width else x
                y1 = max(0, y1)
                x1 = max(0, x1)
                
                tiles.append((x1, y1, tile_size, tile_size))
                
                if x1 + tile_size >= img_width:
                    break
            if y1 + tile_size >= img_height:
                break
                
        return list(set(tiles))

    def _extract_obb_detections(self, result, offset_x, offset_y):
        """Extract oriented bounding box detections"""
        detections = []
        if not hasattr(result, 'obb') or result.obb is None:
            return detections

        obbs = result.obb.xyxyxyxy.cpu().numpy()
        classes = result.obb.cls.cpu().numpy()
        scores = result.obb.conf.cpu().numpy()

        for i in range(len(obbs)):
            poly_points = obbs[i]
            cls = int(classes[i])
            score = float(scores[i])
            
            global_poly = []
            for px, py in poly_points:
                global_poly.append((float(px + offset_x), float(py + offset_y)))
            
            detections.append({
                'polygon': global_poly,
                'class_id': cls,
                'class_name': self.model.names[cls],
                'score': score,
                'type': 'obb'
            })
        return detections

    def _extract_box_detections(self, result, offset_x, offset_y):
        """Extract standard bounding box detections"""
        detections = []
        if not hasattr(result, 'boxes'):
            return detections

        boxes = result.boxes
        for i in range(len(boxes)):
            b = boxes[i].xyxy[0].cpu().numpy()
            cls = int(boxes[i].cls[0])
            score = float(boxes[i].conf[0])
            
            bx1, by1, bx2, by2 = b
            global_poly = [
                (float(bx1 + offset_x), float(by1 + offset_y)),
                (float(bx2 + offset_x), float(by1 + offset_y)),
                (float(bx2 + offset_x), float(by2 + offset_y)),
                (float(bx1 + offset_x), float(by2 + offset_y))
            ]
            
            detections.append({
                'polygon': global_poly,
                'class_id': cls,
                'class_name': self.model.names[cls],
                'score': score,
                'type': 'box'
            })
        return detections

    def _load_image(self, image_path):
        """Load image from GeoTIFF or regular image format"""
        from rasterio.transform import Affine
        
        transform = Affine.identity()

        # Try loading as GeoTIFF first
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with rasterio.open(image_path) as src:
                    band_count = src.count
                    if band_count >= 3:
                        img = src.read([1, 2, 3])
                        img = np.moveaxis(img, 0, -1)
                    elif band_count == 1:
                        band = src.read(1)
                        img = np.stack([band, band, band], axis=-1)
                    else:
                        raise ValueError(f"Unsupported band count: {band_count}")

                    if img is None or img.size == 0:
                        raise ValueError("rasterio returned empty image")

                    src_transform = src.transform
                    if src_transform and src_transform != Affine.identity():
                        transform = src_transform

                    return img, transform
        except Exception:
            pass

        # Fallback: load as regular image with OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot read image: {image_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img, transform

    def run_detection(
        self,
        image_path,
        tile_size=640,
        overlap=0.2,
        conf=None,
        visualize=False,
        output_path=None
    ):
        """
        Run detection on image with optional visualization
        
        Args:
            image_path: Path to input image
            tile_size: Size of detection tiles
            overlap: Overlap ratio between tiles
            conf: Confidence threshold (uses self.conf_threshold if None)
            visualize: Whether to draw boxes on image
            output_path: Path to save visualized image (if visualize=True)
        
        Returns:
            GeoJSON FeatureCollection with detections
        """
        if conf is None:
            conf = self.conf_threshold
            
        img, transform = self._load_image(image_path)
        img_height, img_width = img.shape[:2]
        
        # Create visualization image if needed
        if visualize:
            vis_img = img.copy()
            if vis_img.dtype == np.uint16:  # Convert 16-bit to 8-bit
                vis_img = (vis_img / 256).astype(np.uint8)
        
        tiles = self.get_tiles(img_height, img_width, tile_size, overlap)
        all_detections = []

        print(f"🔍 Processing {len(tiles)} tiles...")
        
        for idx, (tile_x, tile_y, tile_w, tile_h) in enumerate(tiles):
            tile_img = img[tile_y:tile_y + tile_h, tile_x:tile_x + tile_w]
            
            # Run YOLO detection
            results = self.model.predict(
                tile_img,
                conf=conf,
                iou=self.iou_threshold,
                verbose=False
            )

            for result in results:
                # Try OBB first, fallback to boxes
                obb_dets = self._extract_obb_detections(result, tile_x, tile_y)
                if obb_dets:
                    all_detections.extend(obb_dets)
                else:
                    box_dets = self._extract_box_detections(result, tile_x, tile_y)
                    all_detections.extend(box_dets)
        
        print(f"✅ Found {len(all_detections)} detections")
        
        # Draw detections if visualize is enabled
        if visualize and len(all_detections) > 0:
            vis_img = self._draw_detections(vis_img, all_detections)
            
            if output_path:
                # Convert RGB to BGR for OpenCV
                vis_img_bgr = cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR)
                cv2.imwrite(output_path, vis_img_bgr)
                print(f"💾 Visualization saved to: {output_path}")

        return self._build_geojson(all_detections, transform), all_detections

    def _draw_detections(self, img, detections):
        """
        Draw bounding boxes and labels on image
        
        Args:
            img: Input image (RGB)
            detections: List of detection dictionaries
        
        Returns:
            Image with drawn boxes
        """
        img_draw = img.copy()
        
        for det in detections:
            class_id = det['class_id']
            class_name = det['class_name']
            score = det['score']
            polygon = det['polygon']
            
            # Get color for this class
            color = self.colors[class_id % len(self.colors)]
            
            # Convert polygon points to integer
            points = np.array(polygon, dtype=np.int32)
            
            # Draw polygon
            cv2.polylines(img_draw, [points], True, color, 3)
            
            # Fill polygon with semi-transparent color
            overlay = img_draw.copy()
            cv2.fillPoly(overlay, [points], color)
            cv2.addWeighted(overlay, 0.2, img_draw, 0.8, 0, img_draw)
            
            # Prepare label text
            label = f"{class_name}: {score:.2f}"
            
            # Get text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            
            # Draw label background
            label_x, label_y = int(points[0][0]), int(points[0][1])
            cv2.rectangle(
                img_draw,
                (label_x, label_y - text_height - 10),
                (label_x + text_width, label_y),
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                img_draw,
                label,
                (label_x, label_y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
        
        return img_draw

    def _build_geojson(self, detections, transform):
        """Convert pixel-space detections to geographic GeoJSON"""
        features = []
        
        for det in detections:
            geo_points = []
            for px, py in det['polygon']:
                lon, lat = transform * (px, py)
                geo_points.append((float(lon), float(lat)))

            if geo_points:
                geo_points.append(geo_points[0])  # Close the polygon

            feature = geojson.Feature(
                geometry=geojson.Polygon([geo_points]),
                properties={
                    'class': det['class_name'],
                    'confidence': det['score'],
                    'type': det['type']
                }
            )
            features.append(feature)

        return geojson.FeatureCollection(features)


# Example usage
if __name__ == "__main__":
    # Test detection with visualization
    detector = EnhancedSatelliteDetector(
        model_path='yolov8n-obb.pt',
        conf_threshold=0.25,
        iou_threshold=0.45
    )
    
    # Example: detect and visualize
    # geojson_result, detections = detector.run_detection(
    #     image_path='path/to/your/image.tif',
    #     visualize=True,
    #     output_path='detection_result.jpg'
    # )
    
    print("Enhanced detector ready!")
