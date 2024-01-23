from fastapi import FastAPI, File, UploadFile, Response, WebSocket
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64
import datetime

from detect import detect_numberplate, take_picture, get_cropped_images
from ocr import get_text, getOCR
import numpy as np 
import cv2
import os

app = FastAPI()

ENDPOINTS = [
    "/",
    "api/capture"
    "api/detect",
    "api/detect2",
    "api/detect3",
    "ws/detect"
]

origins = [
    "http://localhost",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome!", "endpoints": ENDPOINTS}

@app.get("/api/capture", response_class=Response)
async def capture():
    image = take_picture()
    return Response(image, media_type="image/png")

@app.post("/api/detect")
async def detect(image: UploadFile = File(...)):
    '''
    image: UploadFile = File(...)

    Returns:
        A json response containing the result of the detection
    '''
    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_numberplate(image)
    response = {"result": result}
    return response

@app.post("/api/detect2")
async def detect2(file: UploadFile = File(...)):
    '''
    image: UploadFile = File(...)

    Returns:
        ByteArray of the detected and cropped images
    '''
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    results = get_cropped_images(image)
    images_base64  = [base64.b64encode(chunk).decode('utf-8') for chunk in results]
    print(datetime.datetime.now())
    return JSONResponse(content={"images": images_base64})

@app.post("/api/detect3")
async def detect3(file: UploadFile = File(...)):
    '''
    image: UploadFile = File(...)

    Returns:
        result: A list of dictionaries containing the result of the detection.
        text: A list of strings containing the text detected in the image that matches the pattern of a number plate.
    '''
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_numberplate(image)
    text = getOCR(image, result)
    return JSONResponse(content={"result": result, "text": text})

@app.post("/api/detect_license_plates")
async def detect_license_plates(video: UploadFile = File(...)):
    '''
    video: UploadFile = File(...)

    Returns:
        result: A list of dictionaries containing the result of the license plate detection.
        text: A list of lists containing the OCR text for each frame.
    '''
    video_bytes = await video.read()

    # Save the video temporarily
    temp_video_path = 'temp_video.mp4'
    with open(temp_video_path, 'wb') as temp_video:
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

    # Cleanup: Close VideoCapture and remove the temporary video file
    video_capture.release()
    cv2.destroyAllWindows()
    try:
        os.remove(temp_video_path)
    except OSError:
        pass

    return JSONResponse(content={"result": result_list, "text": text_list})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)