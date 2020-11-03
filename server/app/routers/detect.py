from fastapi import APIRouter, File, UploadFile
from models.Models import DefectDetection
import shutil
import os

router = APIRouter()

defect_detection_model = DefectDetection()

@router.post("/")
async def post_defect_detection(img: UploadFile =File(...)):
    img_name = "temp-img.png"
    with open(img_name, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)

    prediction = defect_detection_model.predict(img_name)

    # TODO: Overlay a bounding box, with label & confidence on the image & return image
    
    os.remove(img_name)
    return prediction


