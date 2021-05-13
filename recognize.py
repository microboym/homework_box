import tensorflow as tf
from tensorflow import keras
import numpy as np

import pre_process

print(f"TensorFLow version {tf.__version__}")
print(f"Keras version {keras.__version__}")
print(f"Numpy version {np.__version__}")

class Recognizer():

    def __init__(self, model_path="model.h5"):
        print("Loading model", model_path)
        self.model = keras.models.load_model(model_path)
        print("Model loaded")

    def predict(self, img, roi=(0, 0, 0, 0), length=5):
        _, _, bin = pre_process.accessBinary(img, roi)
        borders = pre_process.get_borders(bin, length=length)
        number_images = pre_process.extract_numbers(bin, borders)
        results = self.model.predict(number_images)
        numbers = []
        for res in results:
            numbers.append(str(np.argmax(res)))
        return int(''.join(numbers))
