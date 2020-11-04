import cv2
import string
import random


def generate_file_name(num_char=10, prefix="img_", extension=".png"):
    return prefix + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(num_char)]) + extension


def save_img(img, prefix="img_", extension=".png", filename=None):
    if filename == None:
        filename = generate_file_name(prefix=prefix, extension=extension)
    cv2.imwrite(filename, img)
    return filename

def extract_region(img_file, bounding_box, save=True):
    im = cv2.imread(img_file)
    extracted = im[bounding_box[1]:bounding_box[3], bounding_box[0]:bounding_box[2]]
    
    response = {"extracted_img": extracted}

    if save:
        response["filename"] = save_img(extracted)
        # filename = generate_file_name()
        # cv2.imwrite(filename, extracted)
        # response["filename"] = filename
    
    return response

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
            cv2.putText(im, detections[i]["defect_pred"], (b_box[0] - 10, b_box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return im    
