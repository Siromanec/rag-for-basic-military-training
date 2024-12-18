import base64
import os

import cv2
import numpy as np

DATA_PATH = "./data"

CONFIG_PATH = os.path.join(DATA_PATH, "./config.txt")


def read_config_file() -> list[str]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return file.readlines()


def convert_image_to_base64_url(image: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', image)

    return f"data:image/jpg;base64,{base64.b64encode(buffer).decode('utf-8')}"
