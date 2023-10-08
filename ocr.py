import easyocr
from PIL import Image
from detect import get_cropped_images
import numpy as np
import re

reader = easyocr.Reader(['en'])
PATTERN = r"^[a-zA-Z]{2}[0-9]{2}[a-zA-Z]{2}[0-9]{4}$"

def get_text(image, json_results = None):
    """
    image: PIL.Image
    json_results: list

    Returns:
        A list of strings containing the text detected in the image that matches the pattern of a number plate.
    """
    if json_results is not None:
        for r in json_results:
            if r['name'] == 'license-plate':
                x1, y1, x2, y2 = r['box']['x1'], r['box']['y1'], r['box']['x2'], r['box']['y2']
                # print("Coordinates: "+str(x1), y1, x2, y2, sep=", ")
                image2 = image.crop((x1, y1, x2, y2))
                break
    result = reader.readtext(np.array(image2), detail = 0)
    final = []
    if type(result) == list:
        for text in result:
            if re.match(PATTERN, text):
                final.append(text)
    return final