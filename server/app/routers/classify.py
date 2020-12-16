# == API Endpoints for Defect Classification ==

"""
Following are the implementations of the endpoint(s) used for the defect classification process.
It uses the `DefectClassification` model, trained on the [Metal Surface Defects Dataset](https://www.kaggle.com/fantacher/neu-metal-surface-defects-data), & available for use through
the implementation in [models/DefectModels.py](../models/DefectModels.html).
"""

from fastapi import APIRouter, File, UploadFile
from models.DefectModels import DefectClassification
import shutil
import os

router = APIRouter()

defect_classification_model = DefectClassification()

# === Implementation of **POST /classify** Endpoint ===

"""
The function first stores the uploaded image temporarily in the local database of the server & then uses the Defect Classification Model
to predic the type of defect indicated in the image.

**Parameters:**

1. `img`: image file uploaded to the API endpoint using the POST request
"""
@router.post("/")
async def post_defect_classification(img: UploadFile =File(...)):
    img_name = "temp-img.png"
    with open(img_name, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)

    prediction = defect_classification_model.predict(img_name)
    
    os.remove(img_name)
    return prediction