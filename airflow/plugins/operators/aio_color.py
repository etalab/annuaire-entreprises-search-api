import json

import requests

AIO_URL = "http://localhost:4500"


def get_next_color():
    try:
        response = requests.get(AIO_URL + "/colors")
        next_color = json.loads(response.content)["NEXT_COLOR"]
    except requests.exceptions.RequestException:
        next_color = "blue"
    return next_color
