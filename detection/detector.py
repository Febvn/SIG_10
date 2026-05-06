import os
import sys
import cv2
import numpy as np
import rasterio
import geojson
from ultralytics import YOLO


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


class SatelliteDetector:
    def __init__(self, model_path='yolov8n-obb.pt'):
        self.model = YOLO(model_path)

    def get_tiles(self, img_height, img_width, tile_size=640, overlap=0.1):
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
        """Extract detections from OBB result."""
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
                'class_name': self.model.names[cls],
                'score': score
            })
        return detections

    def _extract_box_detections(self, result, offset_x, offset_y):
        """Extract detections from standard boxes result (fallback)."""
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
                'class_name': self.model.names[cls],
                'score': score
            })
        return detections

    def _load_image(self, image_path):
        """Load image and return (numpy_array, affine_transform).
        Handles both GeoTIFF and regular image formats (JPG/PNG)."""
        from rasterio.transform import from_bounds, Affine
        import warnings

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

                    # Use geo-transform if available (non-identity)
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

    def run_detection(self, image_path, tile_size=640, overlap=0.1, conf=0.1):
        img, transform = self._load_image(image_path)

        img_height, img_width = img.shape[:2]
        tiles = self.get_tiles(img_height, img_width, tile_size, overlap)
        all_detections = []

        for (tile_x, tile_y, tile_w, tile_h) in tiles:
            tile_img = img[tile_y:tile_y + tile_h, tile_x:tile_x + tile_w]
            results = self.model.predict(tile_img, conf=conf, verbose=False)

            for result in results:
                obb_dets = self._extract_obb_detections(result, tile_x, tile_y)
                if obb_dets:
                    all_detections.extend(obb_dets)
                else:
                    box_dets = self._extract_box_detections(result, tile_x, tile_y)
                    all_detections.extend(box_dets)

        return self._build_geojson(all_detections, transform)

    def _build_geojson(self, detections, transform):
        """Convert pixel-space detections to geographic GeoJSON."""
        features = []
        for det in detections:
            geo_points = []
            for px, py in det['polygon']:
                lon, lat = transform * (px, py)
                geo_points.append((float(lon), float(lat)))

            if geo_points:
                geo_points.append(geo_points[0])

            feature = geojson.Feature(
                geometry=geojson.Polygon([geo_points]),
                properties={
                    'class': det['class_name'],
                    'confidence': det['score']
                }
            )
            features.append(feature)

        return geojson.FeatureCollection(features)


if __name__ == "__main__":
    pass
