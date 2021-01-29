# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:21:57 2021

@author: crtom
"""
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from tkinter import messagebox as msg

# to display background image inconfiguration
from PIL import Image, ImageTk

from JsonConfig import JsonConfig

class PopupWindowConfiguration(object):
    """
    {"name": "D2",
    "mode": "i",
    "number": "2",
    "type": "d",
    "is_pwm": false,
    "is_analog": false,
    "enabled": true}
    """
    def __init__(self, root):

        self.root = root

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
            # trigger new controls configuration at parent
            self.root.reconfiguration = True

        self.win.destroy()

    def _create_middle_widgets(self):
        load = Image.open("diagram-v2.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.middle_frame, image=render)
        img.image = render
        img.place(x=0, y=0)

    def _create_left_widgets(self):
        # for input/output selectiong
        # (‘i’ for input, ‘o’ for output, ‘p’ for pwm).
        # 1st create frame for the control/indicator
        # each pin will have its own variables

        self.mode_vars = []

        for index, io_pin in enumerate(self.config_data['io_pins']):

            if io_pin['is_analog']:
                # analog pins are in left frame
                frame = self.left_frame
            else:
                # digital pins are in right frame
                frame = self.right_frame

            if io_pin['is_pwm']:
                mode = ["", "Input", "Output", "PWM"] # add "" beacuse of tkk.optionmenu bug
            else:
                mode = ["", "Input", "Output"] #etc

            mode_value = ''
            if io_pin['mode'] == 'i':
                mode_value = 'Input'
            if io_pin['mode'] == 'o':
                mode_value = 'Output'
            if io_pin['mode'] == 'p':
                mode_value = 'PWM'

            mode_var = tk.StringVar()
            mode_var.set(mode_value)
            # mode_var.set(io_pin['mode']) # default value

            self.mode_vars.append(mode_var)
            # print(io_pin)
            self.frame_widget = Frame(frame, bg='white', pady=3, highlightbackground="black", highlightthickness=1)
            self.frame_widget.pack()

            # create lable
            self.mode_lbl = tk.Label(self.frame_widget, text = io_pin['name'], width = 10)
            # create mode
            # print(io_pin['mode'])
            # self.mode_drop = tk.OptionMenu(self.frame_widget, self.mode_vars[index], *mode) # * unpacking
            # self.mode_drop = ttk.OptionMenu(self.frame_widget, self.mode_vars[index], *mode) # * unpacking
            self.mode_drop = ttk.OptionMenu(self.frame_widget, self.mode_vars[index], *mode) # * unpacking
            self.mode_drop.config(width=10)

            # grid
            self.mode_lbl.grid(row=0, column=0)
            self.mode_drop.grid(row=0, column=1)


    def save_configuration(self):
        # translate value of controls to configuration data
        for index, io_pin in enumerate(self.config_data['io_pins']):
            if self.mode_vars[index].get() == 'Input':
                variable = 'i'
            if self.mode_vars[index].get() == 'Output':
                variable = 'o'
            if self.mode_vars[index].get() == 'PWM':
                variable = 'p'
            # change configuration cdictionary values
            self.config_data['io_pins'][index]['mode'] = variable

        # save dictionary to json object file
        self.config_obj.set_data(self.config_data)


def main():
    
    root = tk.Tk()
    
    root.title("app")
    root.geometry("500x500")
    root.attributes("-topmost", True)
    root.lift()
    
    frame = Frame(root, bg="silver")
    frame.pack(side = "right", fill="y", padx = 5, pady = 5)
    PopupWindowConfiguration(root)
    # lbl = tk.Label(frame, text="Hello")
    # lbl.grid(column=0, row=0)
    
    root.mainloop()
#-----------------------------
if __name__ == "__main__":
    main()