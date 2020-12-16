# == Utility Functions ==

"""
Here, we define some utility functions that are used to implement the functionality at the various API endpoints in our server
"""
import cv2
import string
import random

# === Generate a File Name ===

"""
Function to generate a random-looking filename given a prefix & an extension along with the number of characters in the random portion of the filename.

**Parameters:**

1. `num_char` : number of characters in the random portion of the filename (default = 10)
2. `prefix` : prefix of the file (default = "img_")
3. `extension`: file extension required (default = ".png")
"""
def generate_file_name(num_char=10, prefix="img_", extension=".png"):
    return prefix + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(num_char)]) + extension


# === Save an Image ===

"""
Function to generate a filename for an image (if not already provided) & then save it on the server

**Parameters:**

1. `img` : image to be saved
2. `prefix` : prefix of the file (default = "img_")
3. `extension`: file extension required (default = ".png")
4. `filename`: name of the file (should be None if a file name has to be generated)
"""
def save_img(img, prefix="img_", extension=".png", filename=None):
    if filename == None:
        filename = generate_file_name(prefix=prefix, extension=extension)
    cv2.imwrite(filename, img)
    return filename


# === Extract a Region from an Image ===

"""
Function to extract a region from an image file given a bounding box

**Parameters:**

1. `img_file`: name of the image file from which region has to be extracted
2. `bounding box`: opencv type coordinates of the bounding box for selecting the region of interest
3. `save`: boolean indicating if the extracted portion should be saved on the server
"""
def extract_region(img_file, bounding_box, save=True):
    im = cv2.imread(img_file)
    extracted = im[bounding_box[1]:bounding_box[3], bounding_box[0]:bounding_box[2]]
    
    response = {"extracted_img": extracted}

    if save:
        response["filename"] = save_img(extracted)
    
    return response


# === Draw Bounding Boxes for Regions Detected by a Model ===

"""
Function to draw colored bounding boxes around parts detected by the model indicating if the part of defective of fine.
The parts marked *Defective* are bounded by a Red box, while those marked *OK* are bounded using a Green box.

**Parameters:**

1. `img_file`: name of the image file on which bounding boxes have to be drawn
2. `detections`: dictionary of object detections along with their defect markings for the image (produced by the model)
"""
def draw_bounding_boxes(img_file, detections):
    im = cv2.imread(img_file)
    
    for i in detections.keys():
        color = None
        b_box = detections[i]["bounding_box"]
        if detections[i]["defect_pred"] == "OK":
            color = (0, 255, 0)
        elif detections[i]["defect_pred"] == "Defective":
            color =(0, 0, 255)

        if color != None:
            cv2.rectangle(im, (b_box[0], b_box[1]), (b_box[2], b_box[3]), color, 2)
            cv2.putText(im, detections[i]["defect_pred"], (b_box[0] + 10, b_box[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return im    
