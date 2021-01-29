"""
Python GUI with Tkinter
"""

import sys
import time
from datetime import datetime

# main modules imports
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import ttk

from tkinter import Frame
# from tkinter import scrolledtext
# from tkinter import Menu
# from tkinter import messagebox as msg
# from tkinter import Spinbox

import serial
import serial.tools.list_ports

import random

import pyfirmata2
from pyfirmata2 import Arduino

# my files
from JsonConfig import JsonConfig
from PopupWindowConfiguration import PopupWindowConfiguration
from GUI_IO_control import *

APP_TITLE = ("Python GUI Template")
LARGE_FONT = ("Verdana", 12)

class MainGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        # self.pin_configurations = ['d:2:o',
        #              'd:3:o',
        #              'd:4:o',
        #              'd:5:o',
        #              'd:6:i',
        #              'd:7:i',
        #              'd:8:o',
        #              'd:9:o',
        #              'd:10:o',
        #              'd:11:o',
        #              'd:12:o',
        #              'd:13:o',
        #              'a:0:i',
        #              'a:1:i',
        #              'a:2:i',
        #              'a:3:i',
        #              'a:4:i',
        #              'a:5:i']

        self.parent = parent
        self.reconfiguration = False
        self.io_controls = []

        self.is_hardware = False
        # set title
        self.parent.title(APP_TITLE)
        # set icon
        self.parent.iconbitmap("./graphics/python.ico")
        # set size
        self.parent.geometry("500x500")

        # self.parent.bind('<Escape>', self.button_exit_call())

        if self.is_hardware:
            self.port = pyfirmata2.Arduino.AUTODETECT
            print("Setting up the connection to the board ...")
            self.board = pyfirmata2.Arduino(self.port)
            # enable arduino sampling --> for inputs
            # self.board.samplingOn()
        else:
            self.board = None

        #load configuration file
        self.config_obj = JsonConfig('configuration.txt')
        self.pyfirmata_config_list = self.config_obj.get_data(True)
        
        # create main frames
        self.left_frame = Frame(self.parent, bg="silver")
        self.right_frame = Frame(self.parent, bd=2, bg='grey') #bg="silver"

        # show main frames
        self.left_frame.pack(side = "left", fill="y", padx = 5, pady =5)
        self.right_frame.pack(side = "right", fill="y", padx = 5, pady = 5)

        self._create_left_widgets()
        self._create_right_widgets()

        # self._configure_widgets()
        self._run()

        # progress bar counter
        self.progress_cnt = 0
        
        # # after everything is initialized
        # self._reconfigure_widgets()

    def _reconfigure_widgets(self):
        # type:number:mode (a:0:i)
        pass


    def _open_config_win(self):
        # run class
        PopupWindowConfiguration(self)

    def _create_left_widgets(self):
        
        # first load configuration for buttons data
        config_obj = JsonConfig('configuration.txt')
        pyfirmata_config_list = config_obj.get_data(True)
        
        for index, pyfirmata_config in enumerate(pyfirmata_config_list):
            frame = tk.Frame(root, bg="silver")
            # frame.pack(fill="x", padx = 5, pady = 5) #side = "right", 
            frame.pack(fill= tk.BOTH, padx = 5, pady = 5) #side = "right", 
    
            pin_type = pyfirmata_config.split(':')[0]
            pin_number = pyfirmata_config.split(':')[1]
            pin_mode = pyfirmata_config.split(':')[2]
            # digital_input'
            if pin_type == 'd' and pin_mode == 'i':
                control = DigitalInput(root, frame, pin_type, pin_number, pin_mode)
            #'digital_output'
            if pin_type == 'd' and pin_mode == 'o':
                control = DigitalOutput(root, frame, pin_type, pin_number, pin_mode)
            # 'analog_input'    
            if pin_type == 'a' and pin_mode == 'i':
                control = AnalogInput(root, frame, pin_type, pin_number, pin_mode)
            # 'analog_output'
            if pin_type == 'a' and pin_mode == 'o':
                control = AnalogOutput(root, frame, pin_type, pin_number, pin_mode)
            # 'pwm_output'    
            if pin_type == 'p' and pin_mode == 'o': 
                control = PWMOutput(root, frame, pin_type, pin_number, pin_mode)
            
            self.io_controls.append(control)
            
    def _create_right_widgets(self):
        # add progress bar
        self.progress_bar = ttk.Progressbar(self.right_frame, orient="horizontal",
                                        length=300, mode="determinate")
        self.progress_bar.pack()
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 100

        # cofiguration Button widget
        self.config_btn = tk.Button(self.right_frame, text="Configuration", command = self._open_config_win) #
        #Button_Exit.grid(column = 0, row = 0,padx=10,pady=10)
        self.config_btn.pack()

        # Exit Button widget
        self.button_exit = ttk.Button(self.right_frame, text="Exit", command = self.button_exit_call) #
        #Button_Exit.grid(column = 0, row = 0,padx=10,pady=10)
        self.button_exit.pack()

    def _run(self):
        #put it in front of other windows, but not for all the time
        self.parent.attributes("-topmost", True)
        self.parent.lift()
        self.parent.attributes('-topmost',True)

        # will run as soon as the mainloop starts.
        self.parent.after(0, self._update_clock_event)
        self.parent.mainloop()

    def _update_clock_event(self):
        #now = time.strftime(("%H:%M:%S.%f")[:-3])
        now = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        # used to show that app is running
        # this flag is set at first start of app and after setting change
        if self.reconfiguration:
            self.reconfiguration = False
            self._reconfigure_widgets()

        self.update_progress_bar()

        if self.is_hardware:
            pass

        # for gui_io_control in self.gui_io_controls:
        #     gui_io_control.read()

        # call again after 100
        self.parent.after(100, self._update_clock_event)

    def button_exit_call(self):
        print("button_exit_call method executed")
        print("Exit button was pressed")
        # cancel update clock event
        self.parent.after_cancel(self._update_clock_event)
        # close pyfirmata communication
        if self.is_hardware:
            self.board.samplingOff()
            self.board.exit()
        time.sleep(1)
        # close GUI
        self.parent.quit()
        self.parent.destroy()

    def update_progress_bar(self):
        self.progress_bar["value"] += 1
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