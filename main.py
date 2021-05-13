from time import sleep
import tkinter as tk

import data
import status
import interface
# from recognize import Recognizer
from capture import capture_picture
import baidu

# recognizer = Recognizer("./model.h5")
recognizer = baidu

name_list = data.get_name_list()

# Set up interface
root = tk.Tk()
app = interface.Application(master=root, name_list=name_list)


def main():
    # Main Loop
    print("Main Loop")
    while True:
        sleep(2)

        if status.book_passed():
            image = capture_picture()

            # TODO Add ROI
            id = recognizer.predict(image)

            if id is not None:
                print("Got Name: ", id)
                if id in name_list:
                    app.add_submitted(id)


# root.after(1000, main)
app.mainloop()
