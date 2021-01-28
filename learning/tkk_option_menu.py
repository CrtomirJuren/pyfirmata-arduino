import tkinter.ttk as ttk
import tkinter as tk

a = tk.Tk()

options = ['', '1', '2', '3']
value = tk.StringVar()
value.set(options[1])

masterframe = ttk.Frame()
masterframe.pack()

dropdown = ttk.OptionMenu(masterframe, value, *options)
dropdown.pack()

a.mainloop()