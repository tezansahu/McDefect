# Deep Learning Models

Following are the weights for the Deep Neural Models that have been developed as a part of this project:

- __Defect Detection:__ [`defect_detection_vgg16.hdf5`](https://drive.google.com/file/d/16PxIWtCWT-YXCSnk9uNgBQYgxPpoweHm/view?usp=sharing)
- __Defect Classification:__ [`defect_classification_vgg16.hdf5`](https://drive.google.com/file/d/1jTsQ9Mh3r0pzBOIT1yXUeJK6EX5uTmZY/view?usp=sharing)

## Defect Detection & Classification Models

The Defect Detection & Defect Classification Models (for our demo) have been trained using Transfer Learning, with VGG16 as the base model.

The Defect Detection model has been trained on the [Submersible Pump Impeller Defect Dataset](https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product). The entire training can be found in [this notebook](./DefectDetectionVGG.ipynb). We achieve a training accuracy of _92.71 %_ and a test accuracy of _98.88 %_.

The Defect Classification model has been trained on the [Metal Surface Defect Dataset](https://www.kaggle.com/fantacher/neu-metal-surface-defects-data). The entire training can be found in [this notebook](./DefectClassificationVGG.ipynb). We achieve a training accuracy of _91.3 %_ and a test accuracy of _100 %_.

These models can be downloaded and used as follows:

```python
from keras.models import load_model 

MODEL_FILE = "defect_detection_vgg16.hdf5"      # For detection
# MODEL_FILE = "defect_detection_vgg16.hdf5"    # For classification


model = load_model(MODEL_FILE)
```