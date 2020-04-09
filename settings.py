import os
from dotenv import load_dotenv
load_dotenv()


# json_helpers
IMAGE_URL = os.getenv("IMG_ADDRESS")
FACIAL_LANDMARKS = os.getenv("FACIAL_LANDMARKS")
