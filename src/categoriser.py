import cv2
from src.config import Config

class ObjectCategoriser:
    @staticmethod
    def categorise(contour):
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area < Config.SIZE_SMALL:
            return "Small Object", Config.YELLOW
        elif area < Config.SIZE_PERSON:
            return "Person-Sized", Config.RED
        else:
            return "Large Object", Config.ORANGE