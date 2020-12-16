# == API Endpoints for Defect Detection ==

"""
Following are the implementations of the endpoint(s) used for the defect detection process.
It uses the `ObjectDetection` & `DefectDetection` models, trained on the [Submersible Pump Impeller Defect Dataset](https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product), & available for use through
the implementation in [models/ObjectModels.py](../models/ObjectModels.html) & [models/DefectModels.py](../models/DefectModels.html) respectively.
"""


from fastapi import APIRouter, File, UploadFile
from starlette.responses import FileResponse
from pydantic import BaseModel

from models.DefectModels import DefectDetection
from models.ObjectModels import ObjectDetection
import utils.utils as utils

import shutil
import os
import tempfile
import base64

router = APIRouter()

defect_detection_model = DefectDetection()
object_detection_model = ObjectDetection()

class ImageResult(BaseModel):
    mime: str
    image: str

# === Extract a Region of Interest & Predict Defect Presence ===


def extract_region_and_predict(img_name, b_box):
    """
This function extracts the region of interest from the image 
(the area containing the part detected by our Object Detection model)
using the function mentioned in [utils/utils.py](../utils/utils.html). 
    """

    saved_file = utils.extract_region(img_name, b_box)["filename"]

    """
Once extracted, the Defect Detection model is used to predict the 
presence of any defect in the part.
    """
    prediction = defect_detection_model.predict(saved_file)
    os.remove(saved_file)
    return prediction

# === Implementation of POST /detect Endpoint ===


@router.post("/", response_model=ImageResult)
async def post_defect_detection(img: UploadFile =File(...)):
    """
The function first detects all objects present in an image 
& then predicts whether or not each of them is defective

**Parameters:**

1. `img`: image file uploaded to the API endpoint using the POST request
    """

    img_name = "temp-img.png"
    label_req = ["pump_impeller"]


    with open(img_name, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)
    """
It first stores the uploaded image temporarily in the local database 
of the server runs it through our Object Detection pipeline.
    """

    detections = object_detection_model.detect_objects(img_name)
    
    for i in range(len(detections)):
        if detections[i]["label"] in label_req:
            b_box = detections[i]["bounding_box"]
            pred = extract_region_and_predict(img_name, b_box)
            detections[i]["defect_pred"] = pred["prediction"]

    """
The bounding boxes of the detected parts are returned as a dictionary. 
For each detected part, the region of interest is selected using the 
bounding box & a prediction is made as to whether or not it contains 
any defect based on our Defect Detection Model.
    """
    final_img = utils.draw_bounding_boxes(img_name, detections)

    """
These predictions are used to draw colored bounding boxes around the detected parts
    """

    os.remove(img_name)

    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=False) as FOUT:
        utils.save_img(final_img, filename=FOUT.name)
        encoded_image_string = base64.b64encode(FOUT.read())
        return {
            "mime" : "image/png",
            "image": encoded_image_string,
        }

    """
The new image with colored bounding boxes is converted to base64 & returned 
as a string to the client for being displayed
    """
