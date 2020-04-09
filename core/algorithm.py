import cv2
import numpy as np


#import settings

from ..settings import *

# All facial landmarks points from shape predictor


class Algorithm:
    FACIAL_lANDMARKS = {
        "left_eyebrow": [22, 27],
        "right_eyebrow": [17, 22],
        "right_eye": [36, 42],
        "left_eye": [42, 48],
        "nose": [27, 36],
        "mouth": [48, 68],
        "jaw": [0, 17],
    }

    FACIAL_lANDMARKS_X5 = {"right_eye": [1, 2], "left_eye": [3, 4]}

    def haarcascade(self):
        model_location = "./core/models/haarcascade_frontalface_default.xml"
        return cv2.CascadeClassifier(model_location)

    def shape_to_np(self, shape):
        """  """
        cooridinates = np.zeros(
            (shape.num_parts, 2), dtype="int"
        )  # new array filled with zeros
        for x in range(0, shape.num_parts):
            cooridinates[x] = (shape.part(x).x, shape.part(x).y)
        return cooridinates

    def hog_landmarks(self, image, landmarkModal, faceDetetor):
        """ HoG 5 or 68 point algorithm for detecting eyes """

        LANDMARKS = settings.FACIAL_LANDMARKS

        # Get start and end endpoints for eyes
        (lStart, lEnd) = Algorithm.FACIAL_lANDMARKS_X5["left_eye"]
        (rStart, rEnd) = Algorithm.FACIAL_lANDMARKS_X5["right_eye"]

        # Find face - First check if face is frontal
        face = faceDetetor(image, 0)
        if face:

            # Find eyes - Second check if face is frontal
            find_eyes = landmarkModal(image, face[0])
            find_eyes = self.shape_to_np(find_eyes)

            left_eye = find_eyes[lStart:lEnd]
            right_eye = find_eyes[rStart:rEnd]

            if left_eye.size and right_eye.size:
                return "FRONTAL"
            else:
                return "NOT_FRONTAL"
        else:
            return "NOT_FRONTAL"

    def variance_of_laplacian(self, image):
        return cv2.Laplacian(image, cv2.CV_64F).var()
