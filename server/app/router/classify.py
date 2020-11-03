from fastapi import APIRouter, File, UploadFile
from models.Models import DefectClassification
import shutil
import os

router = APIRouter()

defect_classification_model = DefectClassification()

@router.post("/")
async def post_defect_classification(img: UploadFile =File(...)):
    img_name = "temp-img.png"
    with open(img_name, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)

    prediction = defect_classification_model.predict(img_name)

    # TODO: Overlay a bounding box, with label & confidence on the image & return image
    
    os.remove(img_name)
    return prediction