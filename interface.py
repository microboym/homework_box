import tkinter as tk

import data

from capture import capture_picture
import baidu

# recognizer = Recognizer("./model.h5")
recognizer = baidu

class Application(tk.Frame):

    def __init__(self, master=None, name_list=[], submitted=[]):
        super().__init__(master)

        self.name_list = set(name_list)
        self.submitted = set(submitted)

        self.option_add('*Font', '70')

        self.master = master
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.create_widgets()

        w, h = self.master.maxsize()
        self.master.geometry("{}x{}".format(w, h))

    def create_widgets(self):
        self.submitted_box = tk.Listbox(self)
        self.submitted_box.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        for id in list(self.submitted):
            self.submitted_box.insert('end', id)

        self.unsubmitted_box = tk.Listbox(self)
        self.unsubmitted_box.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        for id in list(self.name_list - self.submitted):
            self.unsubmitted_box.insert("end", id)

    def add_submitted(self, id):
        self.submitted = self.submitted | {id}
        self.submitted_box.insert("end", id)

        self.unsubmitted_box.delete(0, tk.END)
        for id in list(self.name_list - self.submitted):
            self.unsubmitted_box.insert("end", id)

    def scan(self):
        image = capture_picture()

        # TODO Add ROI
        id = recognizer.predict(image)

        print(id)
        if id is not None:
            print("Got Name: ", id)
            if id in name_list:
                app.add_submitted(id)

        self.after(1000, self.scan)


# if __name__ == "__main__":
#     name_list = data.get_name_list()

#     root = tk.Tk()
#     app = Application(master=root, name_list=name_list)

#     app.after(1000, app.scan)

#     app.mainloop()
