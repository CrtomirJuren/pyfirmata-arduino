# -*- coding: utf-8 -*-

import tkinter as tk
# from tkinter import Frame, Button, Label
import time

class GUI:

    def __init__(self, root):
        self.root = root # root is a passed Tk object
        self.button = tk.Button(self.root, text="Press to Delete frames", command=self.removethis)
        self.button.pack()
        self.frame_list = []

        self._update_clock_event()

    def create_frame(self):
        frame = tk.Frame(self.root)
        frame.pack()
        label = tk.Label(frame, text="One!")
        label.pack(side = tk.LEFT)
        label = tk.Label(frame, text="Two!")
        label.pack(side = tk.LEFT)
        label = tk.Label(frame, text="Three!")
        label.pack(side = tk.LEFT)
        self.frame_list.append(frame)

    def removethis(self):
        # frame = self.frame_list.pop()
        # self.frame.destroy()

        for frame in self.frame_list:
            # destroy widgets in frame
            for widget in frame.winfo_children():
                widget.destroy()
            # destroy frame
            frame.destroy()

        self.frame_list = []

    def _update_clock_event(self):
        # call again after 100
        self.root.after(1000, self._update_clock_event)
        self.create_frame()

root = tk.Tk()
root.attributes("-topmost", True)
root.lift()

window = GUI(root)


root.mainloop()