from ultralytics import YOLO
import ultralytics
import cv2

cam_port = 0

def take_picture():
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()
    if result:
        cv2.imshow("feed", image)
        cv2.imwrite("feed.png", image)
        cv2.waitKey(0)
    else:
        print("No image detected. Please! try again")

def predict():
    model = YOLO(model='models/best.pt')
    result = model('Sedan-cars-for-road-trips-in-India-1280x720.jpg')
    return result

def main():
    # take_picture()
    result = predict()[0]
    result.save_crop("output")

if __name__ == '__main__':
    main()