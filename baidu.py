from aip import AipOcr
import cv2

APP_ID = '24084707'
API_KEY = 'h3h7GAXsCIwSvXTzLjGjIH6e'
SECRET_KEY = '4MrKfFfMrkGFSTgGqNCp7IeOjojyZENk'

AipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

options = {"detect_direction": "true", "probability": "true"}


def predict(image):
    cv2.imshow("Capture", image)

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    path = "temp.jpg"
    cv2.imwrite(path, image)
    data = get_file_content(path)

    try:
        xx = AipOcr.accurate(data, options)
        xxx = (xx['words_result'])
        xxxx = (xxx[0])
        mdz = (xxxx['words'])
    except:
        return None
    else:
        return mdz