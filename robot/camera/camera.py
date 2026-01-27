
import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        if not self.cap.isOpened():
             # Try to re-open if closed
             self.cap = cv2.VideoCapture(0)
        
        ok, frame = self.cap.read()
        if ok:
            return frame
        return None

# Global Camera Singleton
camera = Camera()
