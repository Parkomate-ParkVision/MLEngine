from ultralytics import YOLO
import cv2
import json
from PIL import Image

cam_port = 0


def take_picture():
    """
    Returns:
        A PIL.Image object containing the picture taken from the webcam.
    """
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()
    cam.release()
    image = Image.fromarray(image)
    image = image.tobytes()
    return image


def detect_numberplate(image):
    """
    image: PIL.Image

    Returns:
        A list of dictionaries containing the result of the detection.
    """
    model = YOLO(model='./models/yolov8-best.pt')
    results = model.predict(image, conf=0.5)
    json_results = results[0].tojson()

    encoded_json_results = str(json_results).replace("\n", '').replace(" ", '')
    encoded_json_results = json.loads(encoded_json_results)
    return encoded_json_results


def get_cropped_images(image):
    """
    image: PIL.Image

    Returns:
        A list of PIL.Image objects containing the cropped images of the
        detected number plates.
    """
    model = YOLO(model='./models/yolov8-best.pt')
    results = model.predict(image, conf=0.5)
    results[0].save_crop("predictions")
    json_results = results[0].tojson()

    encoded_json_results = str(json_results).replace("\n", '').replace(" ", '')
    encoded_json_results = json.loads(encoded_json_results)

    cropped_images = []
    for pred in encoded_json_results:
        x1 = pred['box']['x1']
        y1 = pred['box']['y1']
        x2 = pred['box']['x2']
        y2 = pred['box']['y2']
        cropped_image = image.crop(
            (x1, y1, x2, y2)
        )
        cropped_images.append(cropped_image.tobytes())
    return cropped_images
