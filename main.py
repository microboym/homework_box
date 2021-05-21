# -*- coding: utf-8 -*-

import os
import tkinter as tk

import cnn
import box
import interface

model_path = os.getenv("MODEL_PATH", "model.h5")
server_root = os.getenv("SERVER_URL", "http://127.0.0.1:8000/raspberry")
cam_index = int(os.getenv("CAM_INDEX", "1"))
recognizer = cnn.Recognizer(model_path=model_path)

interface_root = tk.Tk()
interface_root.wm_title("基于AI的智能作业本登记箱")
w, h = interface_root.maxsize()
interface_root.geometry("{}x{}".format(w, h))

# Image frame
imageFrame = tk.Frame(interface_root, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)
imageFrame.pack(side="right")

# Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

raspberry_configs = [
    {"cam_index": cam_index, "servo_pin": 2, "ir_1_pin":3, "ir_2_pin": 4, "tk_label": lmain},
    # {"cam_index": 1, "servo_pin": 2, "ir_1_pin": 3, "ir_2_pin": 4},
]

boxs = [box.Box(recognizer, server_root=server_root, **config) for config in raspberry_configs]

for box in boxs:
    section = interface.Section(interface_root, name_list=[student["name"] for student in box.students])
    box.set_listener(section.update)
    box.start_background()

interface_root.mainloop()
