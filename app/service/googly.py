from random import randint
from typing import Tuple, List

import dlib
from dlib import full_object_detection
from cv2 import ellipse, circle
from numpy import ndarray


class GooglyEyes:
    def __init__(self, predictor_path: str) -> None:
        self.predictor = dlib.shape_predictor(predictor_path)
        self.detector = dlib.get_frontal_face_detector()

    def detect(self, image: ndarray) -> List[Tuple[int, int, int, int]]:
        detections = self.detector(image, 1)
        faces = dlib.full_object_detections()

        for det in detections:
            faces.append(self.predictor(image, det))

        eyes = []
        for face in faces:
            eyes.append(self._extract_eye(face, True))
            eyes.append(self._extract_eye(face, False))

        return eyes

    def googlify(self, eyes: List[Tuple[int, int, int, int]], image: ndarray) -> ndarray:
        for (xi, yi, xj, yj) in eyes:
            # heuristic to set outline thickness of the googly eye based on image size
            outline_thickness = 1 if image.shape[0] < 500 or image.shape[1] < 500 else 2
            center = (xi + xj) // 2, (yi + yj) // 2

            # heuristic used to generate a slightly random googly eye
            # it should cover the entire eye and be slightly random by setting
            # the axes to .2 * largest dimension of the eye
            max_len = max((xj - xi, yj - yi))
            pad = int(max_len * .2)
            axes = randint(max_len, max_len + pad), randint(max_len, max_len + pad)

            # draw eye
            ellipse(image, center, axes, 0., 0., 360, (255, 255, 255), -1)
            ellipse(image, center, axes, 0., 0., 360, (0, 0, 0), outline_thickness)
            circle(image, center, (pad * 3) - 1, (0, 0, 0), -1)

        return image

    def run(self, image: ndarray) -> ndarray:
        eyes = self.detect(image)
        if len(eyes) > 0:
            image = self.googlify(eyes, image)

        return image

    def _extract_eye(self, face: full_object_detection, left: bool) -> Tuple[int, int, int, int]:
        # DLL object detection for the left eye parts are from 36-42
        # and 42-48 for the right eye parts
        parts = range(36, 42) if left else range(42, 48)
        points = [face.part(i) for i in parts]
        return (
            min(points, key=lambda p: p.x).x,
            min(points, key=lambda p: p.y).y,
            max(points, key=lambda p: p.x).x,
            max(points, key=lambda p: p.y).y
        )
