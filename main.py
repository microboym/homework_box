import os
import tkinter as tk

import cnn
import box
import interface

model_path = os.getenv("MODEL_PATH", "model.h5")
server_root = os.getenv("SERVER_URL", "http://127.0.0.1:8000/raspberry")
cam_index = int(os.getenv("CAM_INDEX", "1"))
recognizer = cnn.Recognizer(model_path=model_path)

raspberry_configs = [
    {"cam_index": cam_index, "servo_pin": 2, "ir_1_pin":3, "ir_2_pin": 4},
    # {"cam_index": 1, "servo_pin": 2, "ir_1_pin": 3, "ir_2_pin": 4},
]

boxs = [box.Box(recognizer, server_root=server_root, **config) for config in raspberry_configs]

interface_root = tk.Tk()
for box in boxs:
    section = interface.Section(interface_root, name_list=[student["name"] for student in box.students])
    box.set_listener(section.update)
    box.start_background()

interface_root.mainloop()
