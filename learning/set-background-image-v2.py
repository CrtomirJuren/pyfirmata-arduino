# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:21:34 2021

@author: crtjur
"""
import tkinter as tk

from PIL import Image, ImageTk

root = tk.Tk()
root.title("Title")
root.geometry("280x350")
root.configure(background="black")

class Example(tk.Frame):
    def __init__(self, master, *pargs):
        tk.Frame.__init__(self, master, *pargs)

        self.image = Image.open("diagram-v2.png")
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill= tk.BOTH, expand=True) #,
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)



e = Example(root)
e.pack(fill=tk.BOTH, expand=True)

root.mainloop()