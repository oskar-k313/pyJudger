import logging
import dlib
import numpy as np
import cv2
import time

from cachetools import cached, TTLCache

from .jsonHelpers import inputMessage
from .imageOperation import imageActions, imageHelpers
from .algorithm import Algorithm
from .constants import *


def find_face(img):
    """ Use haarcascade to find face bounding box"""
    algorithm = Algorithm()
    cascade = algorithm.haarcascade()
    faces = cascade.detectMultiScale(img, 1.1, 4)
    # faces = [[10 20 30 40], [50, 60, 70, 80]]
    return faces


@cached(cache={})
def load_landmark_modal():
    """ Cache shape predictor so it doesnt have to be loaded each time """

    try:
        detector = dlib.get_frontal_face_detector()
        model_location = "./core/models/shape_predictor_5_face_landmarks.dat"
        modal = dlib.shape_predictor(model_location)
        return (modal, detector)
    except Exception as err:
        res.media = error_message("Problem loading landmarks modal", err)
        res.status = falcon.HTTP_500
        return False


def laplacian_runner(image, img_type):
    """ Convert img to numpy array, convert to b&w and calculate laplacian """

    if img_type != IMAGE_SIZE.SMALL.value:
        algorithm = Algorithm()

        opencv_img = np.array(image)
        gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
        return algorithm.variance_of_laplacian(gray)
    return 0


def is_frontal_runner(image):
    """ HoG is frontal """

    algorithm = Algorithm()
    opencv_img = np.array(image)
    gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
    cached_model, cached_detector = load_landmark_modal()
    frontal = algorithm.hog_landmarks(gray, cached_model, cached_detector)
    return frontal


def main_runner(body, route):
    """ Extract faces and prepare for qualifying """

    start = time.time()

    img_url = body["url"]
    image_raw = imageActions.get_image(img_url)
    if image_raw is False:
        return False

    np_image = imageActions.get_np_img(image_raw)
    faces = find_face(np_image)
    img_h, img_w = np_image.shape[:2]

    new_body = []
    if route == ROUTER.APPEND.value:
        new_body = body

    for index, face in enumerate(faces):
        imgActions = imageActions()

        img, img_type = imgActions.crop_image(image_raw, face, img_h, img_w)

        # TODO This has to be solved better
        if route == ROUTER.APPEND.value:
            obj = new_body["faces"][index]
            obj[FILTER.LAPLACIAN.value] = laplacian_runner(img, img_type)
            obj[FILTER.ISFRONTAL.value] = is_frontal_runner(img)

        elif route == ROUTER.ALL.value:
            filter = {}
            filter[FILTER.LAPLACIAN.value] = laplacian_runner(img, img_type)
            filter[FILTER.ISFRONTAL.value] = is_frontal_runner(img)
            new_body.append(filter)

        elif route == ROUTER.LAPLACIAN.value:
            filter = {}
            filter[FILTER.LAPLACIAN.value] = laplacian_runner(img, img_type)
            new_body.append(filter)

        elif route == ROUTER.IS_FRONTAL.value:
            filter = {}
            filter[FILTER.ISFRONTAL.value] = is_frontal_runner(img)
            return filter

    end = time.time()
    print("__ TIME __", (end - start))
    return new_body


def health_check_runner():
    return True
