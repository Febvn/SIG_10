from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import os
import shutil
from detection.detector import SatelliteDetector
from detection.detector_enhanced import EnhancedSatelliteDetector
import tempfile
import json

router = APIRouter(prefix="/detection", tags=["Object Detection"])
detector = SatelliteDetector()
enhanced_detector = EnhancedSatelliteDetector(conf_threshold=0.25, iou_threshold=0.45)


@router.post("/process")
async def process_image(
    file: UploadFile = File(...),
    use_enhanced: bool = Query(False, description="Use enhanced detector with better accuracy"),
    conf_threshold: float = Query(0.25, description="Confidence threshold (0.0-1.0)"),
    visualize: bool = Query(False, description="Return visualization image")
):
    """
    Process image for object detection
    
    Parameters:
    - file: Image file (TIF, TIFF, JPG, JPEG, PNG)
    - use_enhanced: Use enhanced detector with visualization support
    - conf_threshold: Confidence threshold for detections
    - visualize: Generate visualization with bounding boxes
    """
    filename = file.filename.lower()
    if not filename.endswith(('.tif', '.tiff', '.jpg', '.jpeg', '.png')):
        msg = "Invalid file type (" + file.filename + "). Only TIF, JPG, PNG allowed."
        raise HTTPException(status_code=400, detail=msg)

    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    vis_path = None
    try:
        if use_enhanced:
            # Use enhanced detector
            if visualize:
                vis_path = tmp_path.replace(os.path.splitext(tmp_path)[1], '_detected.jpg')
                results, detections = enhanced_detector.run_detection(
                    tmp_path,
                    conf=conf_threshold,
                    visualize=True,
                    output_path=vis_path
                )
                
                # Read visualization image and encode as base64
                import base64
                with open(vis_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
                
                return {
                    "geojson": results,
                    "detections_count": len(detections),
                    "visualization": img_data,
                    "visualization_format": "base64_jpeg"
                }
            else:
                results, detections = enhanced_detector.run_detection(
                    tmp_path,
                    conf=conf_threshold
                )
                return {
                    "geojson": results,
                    "detections_count": len(detections)
                }
        else:
            # Use standard detector
            results = detector.run_detection(tmp_path, conf=conf_threshold)
            return results
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Detection failed: " + str(e))
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if vis_path and os.path.exists(vis_path):
            os.remove(vis_path)


@router.get("/classes")
async def get_classes():
    return detector.model.names
