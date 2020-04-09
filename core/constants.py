from enum import Enum


class ROUTER(Enum):
    APPEND = "append"
    ALL = "all"
    LAPLACIAN = "laplacian"
    IS_FRONTAL = "isFrontal"


class IMAGE_SIZE(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class OBJECT_TYPE(Enum):
    FACE = "face"
    PERSON = "person"


class FILTER(Enum):
    LAPLACIAN = "var_laplacian"
    ISFRONTAL = "is_frontal"


class REQUEST(Enum):
    TYPE = "type"
    BBOX = "normalized_bounding_box"
    WIDTH = "width"
    HEIGHT = "height"
