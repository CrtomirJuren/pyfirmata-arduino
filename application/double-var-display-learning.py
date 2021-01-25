# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:32:35 2021

@author: crtom
"""


import tkinter as tk

# --- functions ---

def label_update(a, b, c):
    label["text"] = "{:.0%}".format(myvar.get())

# --- main ---

root = tk.Tk()

myvar = tk.DoubleVar()

label = tk.Label(root)  # without text and textvariable
label.pack()

myvar.trace('w', label_update)  # run `label_update` when `myvar` change value 
myvar.set(0.05)  # set value after `trace`

root.mainloop()