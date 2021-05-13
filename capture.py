import cv2

CAM_NUM = 0

cap = cv2.VideoCapture(CAM_NUM)

def capture_picture():
    _, frame = cap.read()
    print("Captured picture, shape", frame.shape)

    return frame