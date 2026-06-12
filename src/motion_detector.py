import cv2
from src.config import Config

class MotionDetector:
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=Config.BG_HISTORY,
            varThreshold=Config.BG_VAR_THRESHOLD,
            detectShadows=True
        )
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    def detect(self, frame):
        blurred = cv2.GaussianBlur(frame, Config.GAUSSIAN_BLUR, 0)
        mask    = self.bg_subtractor.apply(blurred)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        mask    = cv2.morphologyEx(mask, cv2.MORPH_OPEN,   self.kernel)
        mask    = cv2.morphologyEx(mask, cv2.MORPH_DILATE, self.kernel, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        significant  = [c for c in contours if cv2.contourArea(c) > Config.MIN_CONTOUR_AREA]
        return len(significant) > 0, significant, mask