from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from detection.detector import SatelliteDetector
import tempfile
import json

router = APIRouter(prefix="/detection", tags=["Object Detection"])
detector = SatelliteDetector()


@router.post("/process")
async def process_image(file: UploadFile = File(...)):
    filename = file.filename.lower()
    if not filename.endswith(('.tif', '.tiff', '.jpg', '.jpeg', '.png')):
        msg = "Invalid file type (" + file.filename + "). Only TIF, JPG, PNG allowed."
        raise HTTPException(status_code=400, detail=msg)

    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Run detection
        results = detector.run_detection(tmp_path)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Detection failed: " + str(e))
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.get("/classes")
async def get_classes():
    return detector.model.names
