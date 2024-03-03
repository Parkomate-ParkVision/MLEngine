from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from PIL import Image
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import Response, StreamingResponse
from core.detect import (
    detect_numberplate,
    take_picture,
    get_cropped_images,
    detect_vehicle_type,
    detect_parking_slot,
)
from core.srgan import lp_enhancement
from core.ocr import getOCR, get_similar_number_plates
import cv2
import io
import base64
import os
import json
import tempfile
import matplotlib.pyplot as plt
import re 
import requests
from dotenv import load_dotenv
load_dotenv()


yolorouter = APIRouter(
    responses={404: {"description": "Not found"}},
)


@yolorouter.get("/capture")
async def capture():
    """
    Take a picture using the camera and return the image.

    Returns:
        A response containing the image taken by the camera.
    """
    image = take_picture()
    response = {"image": image}
    return Response(response, media_type="image/png", status_code=200)


@yolorouter.post("/detect")
async def detect(image: UploadFile = File(...)):
    """
    Detects the number plate in the image and returns the result.

    Args:
        image: UploadFile

    Returns:
        A response containing the result of the detection.
    """
    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_numberplate(image)
    response = {"result": result}
    return JSONResponse(content=response, status_code=200)


@yolorouter.post("/detect2")
async def detect2(file: UploadFile = File(...)):
    """
    Detects the number plate in the image and returns the result.

    Args:
        file: UploadFile

    Returns:
        A response containing the result of the detection.
    """
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    results = get_cropped_images(image)
    images_base64 = [base64.b64encode(chunk).decode("utf-8") for chunk in results]
    response = {"images": images_base64}
    return JSONResponse(content=response, status_code=200)


@yolorouter.post("/detect3")
async def detect3(file: UploadFile = File(...)):
    """
    Detects the number plate in the image and returns the result.

    Args:
        file: UploadFile

    Returns:
        A response containing the result of the detection.
    """
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_numberplate(image)
    text = getOCR(image, result)
    response = {"result": result, "text": text}
    return JSONResponse(content=response)


access_token = None
def login():
    global access_token
    if access_token is None:
        email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        payload = {"email": "admin@admin.com", "password": "123"}
        response = requests.post(
            "http://172.22.0.5:8000/login/",
            data=payload,
        )
        access_token = response.json()["tokens"]["access"]
    return access_token


def create_vehicle_instances(number_plates):
    access_token = login()
    headers = {"Authorization": f"Bearer {access_token}"}
    for plate in number_plates:
        response = requests.post(
            "http://172.22.0.5:8000/vehicles/",
            headers=headers,
            data={"number_plate": plate},
        )


@yolorouter.post("/detect4")
async def detect_license_plates(video: UploadFile = File(...)):
    """
    Detects the number plate in the video and returns the result.

    Args:
        video: UploadFile

    Returns:
        A response containing the result of the detection.
    """
    video_bytes = await video.read()

    # Save the video temporarily
    temp_video_path = "temp_video.mp4"
    with open(temp_video_path, "wb") as temp_video:
        temp_video.write(video_bytes)

    # Open the saved video with VideoCapture
    video_capture = cv2.VideoCapture(temp_video_path)

    result_list = []
    text_list = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_results = detect_numberplate(image)
        result_list.extend(frame_results)

        frame_text = getOCR(image, frame_results)
        text_list.append(frame_text)

    number_plates = []
    for i in text_list:
        for j in i:
            if j != []:
                if len(j[0][1]) > 5: 
                    number_plates.append(j[0][1])

    number_plates = [re.sub(r'[^a-zA-Z0-9]', '', plate) for plate in number_plates if plate.strip()]
    number_plates = [re.sub(r'o', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'e', '6', plate) for plate in number_plates]
    number_plates = [re.sub(r'v', 'V', plate) for plate in number_plates]
    number_plates = [re.sub(r's', '5', plate) for plate in number_plates]
    number_plates = [re.sub(r'z', '2', plate) for plate in number_plates]
    number_plates = [re.sub(r'i', '1', plate) for plate in number_plates]
    number_plates = [re.sub(r't', '7', plate) for plate in number_plates]
    number_plates = [re.sub(r'b', '8', plate) for plate in number_plates]
    number_plates = [re.sub(r'g', '9', plate) for plate in number_plates]
    number_plates = [re.sub(r'q', '9', plate) for plate in number_plates]
    number_plates = [re.sub(r'l', '1', plate) for plate in number_plates]
    number_plates = [re.sub(r'd', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'a', '4', plate) for plate in number_plates]
    number_plates = [re.sub(r'c', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'f', '7', plate) for plate in number_plates]
    number_plates = [re.sub(r'h', '4', plate) for plate in number_plates]
    number_plates = [re.sub(r'j', '1', plate) for plate in number_plates]
    number_plates = [re.sub(r'k', '4', plate) for plate in number_plates]
    number_plates = [re.sub(r'm', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'n', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'p', '9', plate) for plate in number_plates]
    number_plates = [re.sub(r'r', '2', plate) for plate in number_plates]
    number_plates = [re.sub(r'u', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'w', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'x', '0', plate) for plate in number_plates]
    number_plates = [re.sub(r'y', '0', plate) for plate in number_plates]

    result = get_similar_number_plates(number_plates)

    create_vehicle_instances(result)

    video_capture.release()
    try:
        os.remove(temp_video_path)
    except OSError:
        pass
    response = {"result": result}
    return JSONResponse(content=response)


@yolorouter.post("/detect5")
async def get_vehicle_type(file: UploadFile = File(...)):
    """
    Detects the vehicle type in the image and returns the result.

    Args:
        file: UploadFile

    Returns:
        A response containing the result of the detection.
    """
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_vehicle_type(image)
    response = {"result": result}
    return JSONResponse(content=response)


@yolorouter.post("/detect6")
async def get_parking_slot(file: UploadFile = File(...)):
    """
    Detects the parking slot in the image and returns the result.

    Args:
        file: UploadFile

    Returns:
        A response containing the result of the detection.
    """
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_parking_slot(image)
    response = {"result": result}
    return JSONResponse(content=response)


@yolorouter.get("/video-feed")
async def video_feed(url: str):
    """
    Streams the video feed from the RTSP URL.

    Args:
        url: str

    Returns:
        A response containing the video feed.
    """
    try:
        if not url.startswith("rtsp://"):
            raise HTTPException(
                status_code=400,
                detail="Invalid RTSP URL format. Should start with 'rtsp://'",
            )

        # Open video capture
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Error opening video stream.")

        # Define the generator function
        def generate():
            while True:
                success, frame = cap.read()
                if not success:
                    break

                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()

                # Construct and yield frame data
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )

        # Return StreamingResponse with correct boundary and media type
        return StreamingResponse(
            generate(), media_type="multipart/x-mixed-replace;boundary=frame"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@yolorouter.get("/lp-extraction")
async def lp_extraction(url: str):
    """
    Gets the video feed and just extracts the license plates. 
    
    Args:
        url: str
        
    Returns:
        A streaming response containing the license plates.
    """
    try:
        if not url.startswith("rtsp://"):
            raise HTTPException(
                status_code=400,
                detail="Invalid RTSP URL format. Should start with 'rtsp://'",
            )
        
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Error opening video stream.")
        
        def generate():
            while True:
                success, frame = cap.read()
                if not success:
                    break
                
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                frame_results = detect_numberplate(image)
                frame_text = getOCR(image, frame_results)
                
                yield (
                    b'Content-Type: application/json\r\n\r\n' +
                    json.dumps({"result": frame_results, "text": frame_text}).encode() +
                    b'\r\n'
                )

        return StreamingResponse(
            generate(), media_type="application/json"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@yolorouter.post("/enhance")
async def enhance(image: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_image:
        temp_image.write(await image.read())

    result = lp_enhancement(temp_image.name)
    os.unlink(temp_image.name)  # Delete the temporary image

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_result_image:
        plt.imsave(temp_result_image.name, result)

    with open(temp_result_image.name, "rb") as result_image_file:
        content = result_image_file.read()

    os.unlink(temp_result_image.name)  # Delete the temporary result image

    return Response(content, media_type="image/jpeg")