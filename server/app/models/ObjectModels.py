import numpy as np
from termcolor import colored
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image

class ObjectDetection:
    def __init__(self, model_file_path="./models/pump_impeller_detection_retinanet.h5", labels=["pump_impeller"]):
        print(colored("INFO", "green"), ": \tLoading Object Detection Model...")
        self.model = models.load_model(model_file_path, backbone_name="resnet50")
        self.threshold = 0.8
        self.labels = {k: v for k, v in enumerate(labels)}
    
    def detect_objects(self, img_file):
        image = read_image_bgr(img_file)

        # preprocess image for network
        image = preprocess_image(image)
        image, scale = resize_image(image)

        boxes, scores, labels = self.model.predict_on_batch(np.expand_dims(image, axis=0))
        
        # correct for image scale
        boxes /= scale

        # store bounding box details for valid detections
        bounding_boxes = {}
        count = 0
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            # scores are sorted so we can break
            if score < self.threshold:
                break

            bounding_boxes[count] = {
                "bounding_box": box.astype(int),
                "label": self.labels[label]
            }
            count += 1
        
        return bounding_boxes

