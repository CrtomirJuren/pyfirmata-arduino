"""
Python GUI with Tkinter
"""

import sys
import time
from datetime import datetime

# main modules imports
import tkinter as tk
from tkinter import ttk

# widget imports
#from tkinter import Stringvar
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Frame
from tkinter import messagebox as msg
from tkinter import Spinbox

import serial
import serial.tools.list_ports

# to display background image inconfiguration
from PIL import Image, ImageTk

import random

import pyfirmata2
from pyfirmata2 import Arduino

# my files
from JsonConfig import JsonConfig


APP_TITLE = ("Python GUI Template")
LARGE_FONT = ("Verdana", 12)

class ConfigurationGUI(object):
    """
    {"name": "D2",
    "mode": "i",
    "number": "2", 
    "type": "d", 
    "is_pwm": false,
    "is_analog": false,
    "enabled": true}
    """
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title('IO Configuration')
        self.win.geometry("680x380")
        # self.win.bind('<Escape>', self._exit_call())
        self.win.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.win.attributes("-topmost", True)
        self.win.lift()

        # create main frames
        self.left_frame = tk.Frame(self.win, width=200, height=350, bg="white")
        self.middle_frame = tk.Frame(self.win, width=280,height=350,bg="white")
        self.right_frame = tk.Frame(self.win, width=200, height=350, bg="white")

        self.left_frame.grid(row=0, column=0)
        self.middle_frame.grid(row=0, column=1)
        self.right_frame.grid(row=0, column=2)

        # load configuration
        self.config_obj = JsonConfig('configuration.txt')
        self.config_data = self.config_obj.get_data(False)
        # print(json_config.get_data(False))
    
        self._create_left_widgets()
        self._create_middle_widgets()
     
    def _on_closing(self):
        if msg.askokcancel("Quit", "Do you want to save new configuration?"):
            self.save_configuration()
        
        self.win.destroy()
        

        
    def _create_middle_widgets(self):
        load = Image.open("diagram-v2.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.middle_frame, image=render)
        img.image = render
        img.place(x=0, y=0)
            
    def _create_left_widgets(self):
        # for input/output selectiong
        mode = ["i","o"] #etc

        # 1st create frame for the control/indicator
        # each pin will have its own variables
        self.mode_vars = []
        for index, io_pin in enumerate(self.config_data['io_pins']):

            mode_var = tk.StringVar()
            mode_var.set(io_pin['mode']) # default value
            self.mode_vars.append(mode_var)
            # print(io_pin)
            self.frame_widget = Frame(self.left_frame, bg='white', pady=3, highlightbackground="black", highlightthickness=1)
            self.frame_widget.pack()
            self.lbl = tk.Label(self.frame_widget, text = io_pin['name'] , width = 10)
            
            self.mode_opt = tk.OptionMenu(self.frame_widget, self.mode_vars[index], *mode)

            self.lbl.grid(row=0, column=0)
            self.mode_opt.grid(row=0, column=1)
    
    def save_configuration(self):
        for index, io_pin in enumerate(self.config_data['io_pins']):
            self.config_data['io_pins'][index]['mode'] = self.mode_vars[index].get()
            
        self.config_obj.set_data(self.config_data)
            
    
        

class GUI_IO_control(tk.Frame):
    def __init__(self, parent, parent_frame, board = None, pin_config = None, *args, **kwargs):
        """
        Parameters
        ----------
        parent : tk.frame
            DESCRIPTION.
        label : TYPE, optional
            DESCRIPTION. The default is None.
        pin_type: string
            digital = ‘d’, analog =‘a’
        pin_number: numeric
        pin_mode: string
            (‘i’ for input, ‘o’ for output, ‘p’ for pwm).

        *args : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent_frame = parent_frame
        self.state = False

        # 1st create frame for the control/indicator
        self.frame = Frame(self.parent_frame, bg='white', pady=3, highlightbackground="black", highlightthickness=1)
        self.frame.pack()

        self.board = board

        if self.parent.is_hardware:
            self.pin_class = self.board.get_pin(pin_config)

            if self.pin_mode == 'i':
                self.pin_class.enable_reporting()

        self.pin_type, self.pin_number, self.pin_mode = pin_config.split(':')
        # print(pin_type, pin_number, pin_mode)



        self.lbl = tk.Label(self.frame, text = self.pin_number, width = 10)



        # if digital output
        if self.pin_type == 'd' and self.pin_mode == 'o':
            self.btn = tk.Button(self.frame, text="Low", relief=tk.SUNKEN, width = 5, command=self.clicked)
            # create frame for the button

        # if digital input
        if self.pin_type == 'd' and self.pin_mode == 'i':
            self.led = tk.Canvas(self.frame, height=25, width=25)
            self.led.create_oval(5,5,20,20, fill='red', tags="led")

        # if analog input
        if self.pin_type == 'a' and self.pin_mode == 'i':
            # initialize variable
            self.string_var = tk.StringVar()
            self.string_var.set('0.00')
            self.value_label = tk.Label(self.frame, width = 5, textvariable = self.string_var)  # without text and textvariable

        # grid
        self.lbl.grid(column=0, row=0)

        if self.pin_type == 'd' and self.pin_mode == 'o':
            self.btn.grid(column=1, row=0)

        if self.pin_type == 'd' and self.pin_mode == 'i':
            self.led.grid(column=1, row=0) #,ipadx="1m",ipady="1m"

        # if analog input
        if self.pin_type == 'a' and self.pin_mode == 'i':
            self.value_label.grid(column=1, row=0)

    def clicked(self):
        if self.btn['text'] == "High":
            self.btn.configure(text="Low", relief=tk.SUNKEN)
            # self.lbl.configure(text="  ON  ", bg="green")
            if self.parent.is_hardware:
                self.pin_class.write(False)
        else:
            self.btn.configure(text="High", relief=tk.RAISED)
            # self.lbl.configure(text="  OFF ", bg="red")
            if self.parent.is_hardware:
                self.pin_class.write(True)

    def read(self):

        # if pin is digital and input
        if self.pin_type == 'd' and self.pin_mode == 'i':
            if self.parent.is_hardware:
                self.state = self.pin_class.read()
            else:
                number = random.uniform(0,100)
                if number > 95:
                    self.state = not self.state

            if self.state:
                colour = 'green'
            else:
                colour = 'red'
            self.led.itemconfig("led", fill = colour)
            self.led.update()

        # if pin is analog and input
        if self.pin_type == 'a' and self.pin_mode == 'i':
            if self.parent.is_hardware:
                analog_value = self.pin_class.read()
            else:
                analog_value = random.uniform(9, 10.0)
                # print(self.pin_class.read())
                display = "{:.4f}".format(analog_value)
                self.string_var.set(display)

class MainGUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.pin_configurations = ['d:2:o',
                     'd:3:o',
                     'd:4:o',
                     'd:5:o',
                     'd:6:i',
                     'd:7:i',
                     'd:8:o',
                     'd:9:o',
                     'd:10:o',
                     'd:11:o',
                     'd:12:o',
                     'd:13:o',
                     'a:0:i',
                     'a:1:i',
                     'a:2:i',
                     'a:3:i',
                     'a:4:i',
                     'a:5:i']

        self.parent = parent

        self.is_hardware = False
        # set title
        self.parent.title(APP_TITLE)
        # set icon
        self.parent.iconbitmap("./graphics/python.ico")
        # set size
        self.parent.geometry("500x500")
        # self.parent.bind('<Escape>', self.button_exit_call())

        # if not self.is_hardware:
        #     # first initiliaze pyfirmata
        #     self.port = pyfirmata2.Arduino.AUTODETECT
        #     print("Setting up the connection to the board ...")
        #     try:
        #         self.board = pyfirmata2.Arduino(self.port)
        #         # enable arduino sampling --> for inputs
        #         self.board.samplingOn()
        #     except serial.SerialException:
        #         print('could not open port')
        if self.is_hardware:
            self.port = pyfirmata2.Arduino.AUTODETECT
            print("Setting up the connection to the board ...")
            self.board = pyfirmata2.Arduino(self.port)
            # enable arduino sampling --> for inputs
            self.board.samplingOn()
        else:
            self.board = None

        # create main frames
        self.left_frame = Frame(self.parent, bg="silver")
        self.right_frame = Frame(self.parent, bd=2, bg='grey') #bg="silver"

        # show main frames
        self.left_frame.pack(side = "left", fill="y", padx = 5, pady =5)
        self.right_frame.pack(side = "right", fill="y", padx = 5, pady = 5)

        self._create_left_widgets()
        self._create_right_widgets()

        self._run()

        # progress bar counter
        self.progress_cnt = 0
        
        
    def _open_config_win(self):
        ConfigurationGUI()

    def _create_left_widgets(self):

        # create one output
        self.gui_io_controls = []

        for pin_config in self.pin_configurations:
            self.gui_io_controls.append(GUI_IO_control(self, self.left_frame, self.board, pin_config))
            # arduino_io_2 = self.board.get_pin('d:2:o')
            # self.io_control_2 = IO_control(self.left_frame, arduino_io_2, 'd:2:o')

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

        # self.parent.after_idle(root.attributes,'-topmost',False)
        # self.parent.after(100, self._run)
        # currently disable periodic call
        # self._update_clock_event()
        # will run as soon as the mainloop starts.
        self.parent.after(0, self._update_clock_event)
        self.parent.mainloop()

    # def quit(self, event):
    #     print("quit method executed")
    #     # cancel update clock event
    #     self.parent.after_cancel(self._update_clock_event)
    #     # close pyfirmata communication
    #     self.board.samplingOff()
    #     self.board.exit()
    #     time.sleep(1)
    #     # close GUI
    #     self.parent.quit()
    #     self.parent.destroy()
    #     exit()

    def _update_clock_event(self):
        #now = time.strftime(("%H:%M:%S.%f")[:-3])
        now = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        # used to show that app is running
        self.update_progress_bar()

        if self.is_hardware:
            pass

        for gui_io_control in self.gui_io_controls:
            gui_io_control.read()

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