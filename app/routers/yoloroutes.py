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
from core.ocr import getOCR
import cv2
import io
import base64
import os


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
    return Response(response, status_code=200)


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

    text_list = [text for text in text_list if text != []]
    # Cleanup: Close VideoCapture and remove the temporary video file
    video_capture.release()
    cv2.destroyAllWindows()
    try:
        os.remove(temp_video_path)
    except OSError:
        pass
    response = {"result": result_list, "text": text_list}
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
        # Validate RTSP URL format (basic check)
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

                # # License plate detection
                # image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                # frame_results = detect_numberplate(image)
                # frame_text = getOCR(image, frame_results)

                # # Encode frame as JPEG
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()

                # Construct and yield frame data
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )

                # Process license plate detection result for this frame
                # yield (b'Content-Type: application/json\r\n\r\n' +
                #        json.dumps({"result": frame_results, "text": frame_text}).encode() +
                #        b'\r\n')

        # Return StreamingResponse with correct boundary and media type
        return StreamingResponse(
            generate(), media_type="multipart/x-mixed-replace;boundary=frame"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
