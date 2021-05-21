import tensorflow as tf
from tensorflow import keras
import numpy as np

import pre_process

print(f"TensorFLow version {tf.__version__}")
print(f"Keras version {keras.__version__}")
print(f"Numpy version {np.__version__}")

class Recognizer():

    def __init__(self, model_path="model.h5", img_roi=(0, 0, 0, 0)):
        print("Loading model", model_path)
        self.model = keras.models.load_model(model_path)
        self.img_roi = img_roi
        print("Model loaded")

    def predict(self, img, length=5):
        try:
            data = pre_process.process_image(img, roi=self.img_roi, min_size=10)
            data = data.astype('float32') / 255
            results = self.model.predict(data)
            numbers = []
            for res in results:
                numbers.append(str(np.argmax(res)))
            return int(''.join(numbers))
        except:
            return None
