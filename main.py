from fastapi import FastAPI, Request, Form, File, UploadFile, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
from PIL import Image
import io
import base64
import datetime

from detect import detect_numberplate, take_picture, get_cropped_images

app = FastAPI()

ENDPOINTS = [
    "/",
    "/capture"
    "/detect",
    "/predict",
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

@app.get("/capture", response_class=Response)
async def capture():
    image = take_picture()
    return Response(image, media_type="image/png")

@app.post("/detect")
async def detect(image: UploadFile = File(...)):
    file_bytes = image.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result = detect_numberplate(image)
    response = {"result": result}
    return response

@app.post("/detect2")
async def detect2(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    results = get_cropped_images(image)
    images_base64  = [base64.b64encode(chunk).decode('utf-8') for chunk in results]
    print(datetime.datetime.now())
    return JSONResponse(content={"images": images_base64})