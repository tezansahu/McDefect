# == RetinaNet-based Model for Object Detection ==

"""
For detecting and segmenting out relevant components (by creating bounding boxes) from in image (or video), we choose to fine-tune the **RetinaNet** (with **ResNet50** Backbone) architecture on our custom dataset(s).
"""

import numpy as np
from termcolor import colored
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image

class ObjectDetection:
    """
Class to wrap around the RetinaNet model & offer the functionality of object detection
    """

    def __init__(self, model_file_path="./models/pump_impeller_detection_retinanet.h5", labels=["pump_impeller"]):

        print(colored("INFO", "green"), ": \tLoading Object Detection Model...")
        """
Load the model & set the detection confidence threshold to 0.8
        """
        self.model = models.load_model(model_file_path, backbone_name="resnet50")
        self.threshold = 0.8
        self.labels = {k: v for k, v in enumerate(labels)}
    
    def detect_objects(self, img_file):
        """
Read & preprocess the image
        """
        image = read_image_bgr(img_file)
        image = preprocess_image(image)
        image, scale = resize_image(image)

        """
Obtain the bounding boxes for the objects detected in the image & correct their scale
        """
        boxes, scores, labels = self.model.predict_on_batch(np.expand_dims(image, axis=0))
        boxes /= scale

        """
Store bounding box details for valid detections (confidence > threshold)
        """
        bounding_boxes = {}
        count = 0
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            """            
Scores are sorted in descending order so that we can `break` on reaching below threshold
            """
            if score < self.threshold:
                break

            bounding_boxes[count] = {
                "bounding_box": box.astype(int),
                "label": self.labels[label]
            }
            count += 1
        
        return bounding_boxes

