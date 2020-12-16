# == VGG16-based Models for Defect Detection & Classification ==

"""
The Defect Detection & Defect Classification Models (for our demo) have been trained using Transfer Learning, with **VGG16** as the base model.
"""

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from termcolor import colored

# === Defect Detection Model ===

"""
The Defect Detection model has been trained on the [Submersible Pump Impeller Defect Dataset](https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product). 
"""

class DefectDetection:

    """
Class to wrap around the VGG16-based model & offer the functionality of defect detection.
    """

    def __init__(self, model_file_path="./models/defect_detection_vgg16.hdf5"):
        print(colored("INFO", "green"), ": \tLoading Defect Detection Model...")
        """
Load the model & set the image width, height & prediction labels.
        """
        self.model = load_model(model_file_path)
        self.WIDTH = 224
        self.HEIGHT = 224
        self.labels = {
            0: "Defective",
            1: "OK"
        }
        

    def predict(self, img_file):
        """
Load & preprocess the image.
        """
        img = image.load_img(img_file, target_size=(self.WIDTH, self.HEIGHT))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        """
Run the image through the defect detection model to obtain its predictions.
        """
        conf = self.model.predict(x)
        prediction = np.argmax(conf[0])
        print(self.labels[prediction])
        return {"prediction": self.labels[prediction]}


# === Defect Classification Model ===

"""
The Defect Classification model has been trained on the [Metal Surface Defect Dataset](https://www.kaggle.com/fantacher/neu-metal-surface-defects-data). 
"""

class DefectClassification:

    """
Class to wrap around the VGG16-based model & offer the functionality of defect classification.
    """

    def __init__(self, model_file_path="./models/defect_classification_vgg16.hdf5", labels=None):
        print(colored("INFO", "green"), ": \tLoading Defect Classification Model...")
        """
Load the model & set the image width, height & prediction labels (6 types of defects here according to the dataset)
        """
        self.model = load_model(model_file_path)
        self.WIDTH = 224
        self.HEIGHT = 224
        if labels == None:
            self.labels = {
                0: 'Crazing', 
                1: 'Inclusion', 
                2: 'Patches', 
                3: 'Pitted', 
                4: 'Rolled',
                5: 'Scratches'
            }
        else:
            self.labels = labels

    def predict(self, img_file):
        """
Load & preprocess the image.
        """
        img = image.load_img(img_file, target_size=(self.WIDTH, self.HEIGHT))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        """
Run the image through the defect classification model to obtain its predictions.
        """
        conf = self.model.predict(x)
        prediction = np.argmax(conf[0])
        return {"prediction": self.labels[prediction]}
