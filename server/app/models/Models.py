from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

class DefectDetection:
    def __init__(self, model_file_path="./models/defect_detection_vgg16.hdf5"):
        self.model = load_model(model_file_path)
        self.WIDTH = 224
        self.HEIGHT = 224
        self.labels = {
            0: "Defective",
            1: "OK"
        }

    def predict(self, img_file):
        img = image.load_img(img_file, target_size=(self.WIDTH, self.HEIGHT))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        conf = self.model.predict(x)
        prediction = np.argmax(conf[0])
        return {"prediction": self.labels[prediction]}

class DefectClassification:
    def __init__(self, model_file_path="./models/defect_classification_vgg16.hdf5", labels=None):
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
        img = image.load_img(img_file, target_size=(self.WIDTH, self.HEIGHT))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        conf = self.model.predict(x)
        prediction = np.argmax(conf[0])
        return {"prediction": self.labels[prediction]}
