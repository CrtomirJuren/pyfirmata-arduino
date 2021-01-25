"""
Python GUI with Tkinter
"""

import sys
import time
from datetime import datetime

# main modules imports
# import tkinter as tk
if(sys.version_info[0]<3):
  # from Tkinter import *
  import Tkinter as tk
else:
  # from tkinter import *
  import tkinter as tk

from tkinter import ttk

# widget imports
#from tkinter import Stringvar
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Frame
from tkinter import messagebox as msg
from tkinter import Spinbox

import serial.tools.list_ports

from PIL import Image, ImageTk

APP_TITLE = ("Python GUI Template")
LARGE_FONT = ("Verdana", 12)

def popup_bonus():
    win = tk.Toplevel()
    win.wm_title("Window")

    l = tk.Label(win, text="Input")
    # l.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    # b.grid(row=0, column=1)

    image = Image.open("./graphics/arduino-uno.png")
    # self.img_copy= self.image.copy()
    image = image.resize((200, 200))

    background_image = ImageTk.PhotoImage(image)

    background = tk.Label(win, image=background_image)
    background.pack(fill=tk.BOTH, expand= False)
    # background.grid(row=1, column=0, columnspan = 2)
    # self.background.bind('<Configure>', self._resize_image)
    # self.background.pack(fill=tk.BOTH, expand=YES)


class MainGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # set title
        self.parent.title(APP_TITLE)
        # set icon
        self.parent.iconbitmap("./graphics/python.ico")
        # set size
        self.parent.geometry("1280x800")
        # Fixing the window size
        self.parent.resizable(width=False, height=False)
        # create main frames

        self.left_frame = Frame(self.parent, width=100, height=500, bg="red")
        self.middle_frame = Frame(self.parent, width=100, height=500, bg="green")
        self.right_frame = Frame(self.parent,  width=100, height=500, bg="blue")

        self._create_widgets()

        # show main frames
        # self.left_frame.pack(fill="y", padx = 5, pady =5) #side = "left",
        # self.middle_frame.pack(fill="y", padx = 5,pady = 5) #side = "left",
        # self.right_frame.pack(fill="y", padx = 5, pady = 5) #side = "right",
        self.left_frame.grid(row=0, column=0, padx = 1, pady =1) #side = "left",
        self.middle_frame.grid(row=0, column=1, padx = 1,pady = 1) #side = "left",
        self.right_frame.grid(row=0, column=2, padx = 1, pady = 1) #side = "right",

        self._run()

        # progress bar counter
        self.progress_cnt = 0
    def app_configure(self):
        pass

    def _open_config_window(self):
        window = tk.Tk()
        window.title("Pin Configuration")
        # set icon
        window.iconbitmap("./graphics/python.ico")
        # set size
        window.geometry("400x400")


    def _middle_frame_widgets(self):
        # Frame.__init__(self, master, *pargs)


        pass

    def _create_widgets(self):

        # create middle frame
        self._middle_frame_widgets()

        # combox for selecting arduino com
        self.port_select_cb = ttk.Combobox(self.right_frame, values=self.get_serial_ports())
        self.port_select_cb.pack(fill = tk.BOTH)

        # assign function to combobox
        self.port_select_cb.bind('<<ComboboxSelected>>', self.on_select)

        # Exit Button widget
        self.button_exit = tk.Button(self.right_frame, text="Exit", command = self.button_exit_call) #
        #Button_Exit.grid(column = 0, row = 0,padx=10,pady=10)
        self.button_exit.pack()

        # Exit Button widget
        self.button_configure = tk.Button(self.right_frame, text="Configure", command = popup_bonus) #
        #Button_Exit.grid(column = 0, row = 0,padx=10,pady=10)
        self.button_configure.pack()

        # add progress bar
        self.progress_bar = ttk.Progressbar(self.right_frame, orient="horizontal",
                                        length=300, mode="determinate")
        self.progress_bar.pack()
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100

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
        self.parent.after(100, self._update_clock_event)
        # used to show that app is running
        self.update_progress_bar()

    def button_exit_call(self):
        print("Exit button was pressed")
        self.parent.quit()
        self.parent.destroy()

    def update_progress_bar(self):
        self.progress_bar["value"] = self.progress_bar["value"] + 1
        if self.progress_bar["value"] >= self.progress_bar["maximum"]:
            self.progress_bar["value"] = 0
        #self.progressbar = self.progress_cnt + 1
 		#self.progress_bar["value"] = self.progress_cnt
   		#self.progress_bar.update()
    	#progress_bar["value"] = 0
        return

    def get_serial_ports(self):
        return serial.tools.list_ports.comports()

    def on_select(self, event=None):
        # get selection from event
        # print("event.widget:", event.widget.get())
        # or get selection directly from combobox
        print("comboboxes: ", self.port_select_cb.get())

#-----------------------------
#----------MAIN LOOP----------
#-----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    # MainGUI(root).pack(side="top", fill="both", expand=True)
    app = MainGUI(root)