import cv2
import os

class FaceDetector:
    def __init__(self, cascade_path=None):
        # Use OpenCV's default haarcascade if not provided
        if cascade_path is None:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Cascade file not found: {cascade_path}")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def detect(self, frame):
        # frame: RGB numpy array
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
        return (len(faces) > 0, faces) 