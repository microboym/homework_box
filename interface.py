# -*- coding: UTF-8 -*-

import tkinter as tk
 
class Section(tk.Frame):

    def __init__(self, master=None, name_list=[], submitted=[]):
        super().__init__(master)

        self.name_list = name_list
        self.submitted = submitted

        self.master = master
        self.pack(expand=tk.YES, fill=tk.Y, side="right")
        self.create_widgets()

    def create_widgets(self):
        self.subject_name = tk.Label(self, text="作业登记", font=("Helvetica", 37))
        self.subject_name.pack(side="top")
        self.lists_frame = tk.Frame(self)
        self.lists_frame.pack(side="bottom", expand=tk.YES, fill=tk.Y)

        font = ("Helvetica", 20)
        self.submitted_box = tk.Listbox(self.lists_frame, font=font)
        self.submitted_box.pack(side="left", expand=tk.YES, fill=tk.Y)
        self.unsubmitted_box = tk.Listbox(self.lists_frame, font=font)
        self.unsubmitted_box.pack(side="right", expand=tk.YES, fill=tk.Y)

        self.update()

    def update(self, submitted=None):
        if submitted is not None:
            self.submitted = submitted

        self.submitted_box.delete(0, tk.END)
        for id in self.submitted:
            self.submitted_box.insert(tk.END, id)

        self.unsubmitted_box.delete(0, tk.END)
        for id in self.name_list:
            if id not in self.submitted:
                self.unsubmitted_box.insert(tk.END, id)
    
    def add(self, id):
        if id not in self.submitted:
            self.submitted.append(id)
            print("ID", id, "\n", "submitted", self.submitted)
        self.update()


if __name__ == "__main__":

    root = tk.Tk()

    section1 = Section(master=root, name_list=["Tony", "Andy", "Tom"], submitted=["Jack"])
    section2 = Section(master=root, name_list=["Tony", "Andy", "Tom"], submitted=["Tony"])

    w, h = root.maxsize()
    root.geometry("{}x{}".format(w, h))

    root.after(2000, lambda: section1.add("Tony"))
    root.after(4000, lambda: section1.add("Andy"))

    root.mainloop()
