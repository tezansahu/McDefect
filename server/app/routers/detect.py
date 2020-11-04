from fastapi import APIRouter, File, UploadFile
from starlette.responses import FileResponse

from models.DefectModels import DefectDetection
from models.ObjectModels import ObjectDetection
import utils.utils as utils

import shutil
import os
import tempfile

router = APIRouter()

defect_detection_model = DefectDetection()
object_detection_model = ObjectDetection()

def extract_region_and_predict(img_name, b_box):
    saved_file = utils.extract_region(img_name, b_box)["filename"]
    prediction = defect_detection_model.predict(saved_file)
    # prediction = defect_detection_model.predict(img_name)
    os.remove(saved_file)
    return prediction

@router.post(
    "/", 
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return image with objects arked as Defective of OK",
        }
    },
)
async def post_defect_detection(img: UploadFile =File(...)):
    img_name = "temp-img.png"
    label_req = ["pump_impeller"]

    with open(img_name, "wb") as buffer:
        shutil.copyfileobj(img.file, buffer)

    detections = object_detection_model.detect_objects(img_name)
    
    for i in range(len(detections)):
        if detections[i]["label"] in label_req:
            b_box = detections[i]["bounding_box"]
            pred = extract_region_and_predict(img_name, b_box)
            detections[i]["defect_pred"] = pred["prediction"]

    final_img = utils.draw_bounding_boxes(img_name, detections)

    os.remove(img_name)

    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=False) as FOUT:
        # FOUT.write(final_img)
        utils.save_img(final_img, filename=FOUT.name)
        return FileResponse(FOUT.name, media_type="image/png")


