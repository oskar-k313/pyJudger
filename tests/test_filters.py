import pytest
import requests
from PIL import Image

from falcon import testing

from source.core.app import Filter

from source.core.imageOperation import imageActions

class TestValidateFilterRoute:
    def test_call_existing_filter_endpoint(self):
        append = "append"
        all = "all"
        laplacian = "laplacian"
        is_frontal = "isFrontal"

        filter = Filter()

        assert filter.validate_route(append) == True
        assert filter.validate_route(all) == True
        assert filter.validate_route(is_frontal) == True

    def test_call_invalid_filter_endpoint(self):

        chocolate = 'chocolate'

        filter = Filter()

        assert filter.validate_route(chocolate) == False


    def test_image_failed_to_downloand(self):
        img = 'https://upload.wikimedia.org/wikipedia/en/3/3f/Pok%C3%A9mon_Magikarp_art.pn'
        imgAction = imageActions()

        assert imgAction.get_image(img) == False

    def test_crop_image_large(self):
        img_url = 'https://upload.wikimedia.org/wikipedia/en/3/3f/Pok%C3%A9mon_Magikarp_art.png'
        response = requests.get(img_url, stream=True)
        response.raw.decode_content = True
        image = Image.open(response.raw)

        coords_large = (0, 0, 200, 200, 228, 203)
        coords_medium = (0, 0, 70, 70, 100, 100)
        coords_small = (0, 0, 40, 40, 75, 75)

        imgAction = imageActions()
        cropped_img, size_large =  imgAction.crop_image(image, coords_large)
        cropped_img, size_medium =  imgAction.crop_image(image, coords_medium)
        cropped_img, size_small =  imgAction.crop_image(image, coords_small)

        assert size_large == 'large'
        assert size_medium == 'medium'
        assert size_small == 'small'
