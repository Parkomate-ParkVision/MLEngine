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
from ocr import get_text

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
async def detect2(file: UploadFile = File(...)):
    '''
    image: UploadFile = File(...)

    Returns:
        result: A list of dictionaries containing the result of the detection.
        text: A list of strings containing the text detected in the image that matches the pattern of a number plate.
    '''
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_numberplate(image)
    text = get_text(image, result)
    print(datetime.datetime.now())
    return JSONResponse(content={"result": result, "text": text})

@app.post("/ws/detect")
async def websocket_endpoint(websocket: WebSocket):
    '''
    websocket: WebSocket

    Returns:
        Stream of the detected and cropped images
    '''
    await websocket.accept()
    while True:
        frame_data = await websocket.receive_bytes()
        image = Image.open(frame_data)
        results = get_cropped_images(image)
        images_base64  = [base64.b64encode(chunk).decode('utf-8') for chunk in results]
        await websocket.send_bytes(images_base64)