from .constants import REQUEST, IMAGE_ADDRESS


class inputMessage:
    @staticmethod
    def get_objects(input_msg):
        return input_msg["objects"]

    @staticmethod
    def get_img_url(input_msg):
        full_element = input_msg["url"]
        get_url = full_element[: full_element.index(".jpg")]
        url = get_url + ".jpg"
        print(url)
        return url

    @staticmethod
    def get_img_dimensions(input_msg):
        h = input_msg[REQUEST.HEIGHT.value]
        w = input_msg[REQUEST.WIDTH.value]
        return h, w
