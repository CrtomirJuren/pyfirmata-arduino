# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:50:18 2021

@author: crtjur
"""
from tkinter import *

# pip install pillow
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = Image.open("diagram-v2.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("280x350") # picture size
root.mainloop()