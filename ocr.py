import easyocr
from PIL import Image
from detect import get_cropped_images
import numpy as np
import re
import cv2

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
                image2 = image.crop((x1, y1, x2, y2))
                break
    result = reader.readtext(np.array(image2), detail = 0)
    final = []
    if type(result) == list:
        for text in result:
            if re.match(PATTERN, text):
                final.append(text)
    return final

def getOCR(image, results):
    ocr_texts = []

    for result in results:
        if result['name'] == 'license-plate':
            x1, y1, x2, y2 = (
                int(result['box']['x1']),
                int(result['box']['y1']),
                int(result['box']['x2']),
                int(result['box']['y2'])
            )
            
            # Crop the license plate region
            plate_image = image.crop((x1, y1, x2, y2))

            # Convert the cropped image to OpenCV format
            plate_image_cv = np.array(plate_image)

            # Convert image to grayscale
            gray = cv2.cvtColor(plate_image_cv, cv2.COLOR_RGB2GRAY)

            # Use the original OCR mechanism
            results = reader.readtext(gray)
            for result in results:
                if len(result) > 1 and len(result[1]) > 0:
                    print(result[1])
                    ocr_texts.append(result[1])

    return ocr_texts