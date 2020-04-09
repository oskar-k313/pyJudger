import requests
import cv2

import numpy as np

from PIL import Image
from .constants import IMAGE_SIZE


class imageActions:
    @staticmethod
    def get_image(img_url):
        """ Downland image from url"""

        try:
            response = requests.get(img_url, stream=True)
            response.raw.decode_content = True
            return Image.open(response.raw)

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_np_img(img):
        """ Translate raw image to numpy array """

        img_arr = np.array(img)
        return cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def crop_image(img, coords, height, width):
        """ Crop image to object Classify as small large or medium  """

        x, y, w, h = coords
        coordinates = (x, y, (x + w), (y + h))

        cropped_image = img.crop(coordinates)
        print(coordinates)

        if (height <= 80) or (width <= 80):
            return (img, IMAGE_SIZE.SMALL.value)

        elif (height >= 140) or (width >= 140):
            cropped_image = cropped_image.resize((120, 120), Image.NEAREST)
            return (cropped_image, IMAGE_SIZE.LARGE.value)

        else:
            cropped_image = cropped_image.resize((120, 120), Image.NEAREST)
            return (cropped_image, IMAGE_SIZE.MEDIUM.value)


class imageHelpers:
    def check_image_size(self, coords):
        """ Calculate width and height of face box"""

        height = coords[3] - coords[1]
        width = coords[2] - coords[0]

        return height, width

    def convert_bbox_to_pixel(self, bounding_box, img_width, img_height):
        """ Convert bounding box from request, to pixel required by Pil """

        xmin, xmax, ymin, ymax = (
            bounding_box["x_min"],
            bounding_box["x_max"],
            bounding_box["y_min"],
            bounding_box["y_max"],
        )

        left = round(xmin * (img_width - 1)) + 1
        right = round(xmax * (img_width - 1)) + 1

        top = round(ymin * (img_height - 1)) + 1
        bottom = round(ymax * (img_height - 1)) + 1

        box_in_pixels = (left, top, right, bottom)
        height_org, width_org = self.check_image_size(box_in_pixels)

        height = height_org * 0.15
        width = width_org * 0.15

        left = left + width
        right = right - width
        top = top + height
        bottom = bottom - height

        return (left, top, right, bottom, height_org, width_org)
