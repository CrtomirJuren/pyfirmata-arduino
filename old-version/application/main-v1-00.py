"""
Python GUI with Tkinter
"""
# main modules imports
import tkinter as tk
from tkinter import ttk

# widget imports
#from tkinter import Stringvar
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Frame
from tkinter import messagebox as msg

import time
from datetime import datetime

APP_TITLE = ("Python GUI Template")
LARGE_FONT = ("Verdana", 12)

class MainGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # set title
        self.parent.title(APP_TITLE)
        # set icon
        self.parent.iconbitmap("./graphics/python.ico")
        # set size
        self.parent.geometry("500x500")

        self._create_widgets()
        self._run()

    def _create_widgets(self):
            pass

    def _run(self):
        #put it in front of other windows, but not for all the time
        self.parent.attributes("-topmost", True)
        self.parent.lift()
        self.parent.attributes('-topmost',True)
        self.parent.after_idle(root.attributes,'-topmost',False)

        self._update_clock_event()
        self.parent.mainloop()

    def quit(self, event):
        self.parent.quit()
        self.parent.destroy()
        exit()

    def _update_clock_event(self):
        #now = time.strftime(("%H:%M:%S.%f")[:-3])
        now = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        self.parent.after(500, self._update_clock_event)

#-----------------------------
#----------MAIN LOOP----------
#-----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    # MainGUI(root).pack(side="top", fill="both", expand=True)
    app = MainGUI(root)