import base64

import cv2
import numpy as np


def convert_image_to_base64_url(image: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', image)

    return f"data:image/jpg;base64,{base64.b64encode(buffer).decode('utf-8')}"
