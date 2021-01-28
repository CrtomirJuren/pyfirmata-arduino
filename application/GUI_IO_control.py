# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:23:45 2021

@author: crtom
"""
try:
    import Tkinter as tk
except:
    import tkinter as tk
from tkinter import ttk
from tkinter import Frame

from JsonConfig import JsonConfig

class GUI_IO_control(tk.Frame):
    def __init__(self, parent, parent_frame, board = None, pin_config = None, *args, **kwargs):
        # each widget has its own variable so it can be easily configured
        # self.mode_vars = []
        self.mode_var = tk.StringVar()
        self.string_var = tk.StringVar()

        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent_frame = parent_frame
        self.state = False

        # 1st create frame for the control/indicator
        self.frame = Frame(self.parent_frame, bg='white', pady=3, highlightbackground="black", highlightthickness=1)
        self.frame.pack(fill=tk.X)

        self.board = board

        if self.parent.is_hardware:
            self.pin_class = self.board.get_pin(pin_config)

            if self.pin_mode == 'i':
                self.pin_class.enable_reporting()

        self.pin_type, self.pin_number, self.pin_mode = pin_config.split(':')
        # print(pin_type, pin_number, pin_mode)

        self.lbl = tk.Label(self.frame, text = self.pin_number, width = 5)
        self.mode_lbl = tk.Label(self.frame, width = 5, textvariable = self.mode_var)  # without text and textvariable


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
            self.string_var.set('0.00')
            self.value_label = tk.Label(self.frame, width = 5, textvariable = self.string_var)  # without text and textvariable

        # grid
        self.lbl.grid(row=0, column=0)
        self.mode_lbl.grid(row = 0, column = 1)

        if self.pin_type == 'd' and self.pin_mode == 'o':
            self.btn.grid(column=2, row=0)

        if self.pin_type == 'd' and self.pin_mode == 'i':
            self.led.grid(column=2, row=0) #,ipadx="1m",ipady="1m"

        # if analog input
        if self.pin_type == 'a' and self.pin_mode == 'i':
            self.value_label.grid(column=2, row=0)

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

    def configure(self, pyfirmata_config):
        print(pyfirmata_config)

        # self.mode_var.set(mode_value)

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


class GUI_IO_control2(tk.Frame):
    def __init__(self, parent, parent_frame, *args, **kwargs):

        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent_frame = parent_frame
        self.state = False

        # 1st create frame for the control/indicator
        self.frame = Frame(self.parent_frame, bg='white', pady=3, highlightbackground="black", highlightthickness=1)
        self.frame.pack(fill=tk.X)

        # each widget has its own variable so it can be easily configured
        # self.mode_vars = []
        self.pin_number_lbl_var = tk.StringVar()
        self.pin_mode_lbl_var = tk.StringVar()
        self.string_var = tk.StringVar()
        
        # self.string_var.set('0.00')
        self.pin_number_lbl_var.set('')
        self.pin_mode_lbl_var.set('')

        # pin number: label
        # self.lbl = tk.Label(self.frame, text = self.pin_number, width = 5)
        self.pin_number_lbl = tk.Label(self.frame, width = 5, textvariable = self.pin_number_lbl_var)
        # mode: label
        self.pin_mode_lbl = tk.Label(self.frame, width = 5, textvariable = self.pin_mode_lbl_var)  # without text and textvariable
        # output control: button
        self.pin_state_btn = tk.Button(self.frame, text="Low", relief=tk.SUNKEN, width = 5, command=self.clicked)
        # digital input led: canvas
        self.led = tk.Canvas(self.frame, height=25, width=25)
        self.led.create_oval(5,5,20,20, fill='red', tags="led")
        # analog input indicator
        self.value_label = tk.Entry(self.frame, width = 5, textvariable = self.string_var)  # without text and textvariable
        # analog output control

        # if digital input
        # if self.pin_type == 'd' and self.pin_mode == 'i':
        # if self.pin_type == 'd' and self.pin_mode == 'o':
        # if self.pin_type == 'a' and self.pin_mode == 'i':
        # if self.pin_type == 'a' and self.pin_mode == 'o':
        # if self.pin_type == 'p' and self.pin_mode == 'o':

        # grid
        self.pin_number_lbl.grid(row=0,column=0)
        self.pin_mode_lbl.grid(row=0,column=1)
        self.pin_state_btn.grid(row=0,column=2)
        self.led.grid(row=0,column=3)
        self.value_label.grid(row=0,column=4)

    def clicked(self):
        if self.pin_state_btn['text'] == "High":
            self.pin_state_btn.configure(text="Low", relief=tk.SUNKEN)
            # self.lbl.configure(text="  ON  ", bg="green")
            if self.parent.is_hardware:
                self.pin_class.write(False)
        else:
            self.pin_state_btn.configure(text="High", relief=tk.RAISED)
            # self.lbl.configure(text="  OFF ", bg="red")
            if self.parent.is_hardware:
                self.pin_class.write(True)

    def configure(self, pyfirmata_config):
        # Button has three states : active, normal, disabled
        # print(pyfirmata_config)        
        self.pin_type, self.pin_number, self.pin_mode = pyfirmata_config.split(':')
        
        self.pin_number_lbl_var.set(self.pin_number)
        pin_mode = ''
        if self.pin_mode == 'i':
            pin_mode = 'IN'
        if self.pin_mode == 'o':
            pin_mode = 'OUT'
        if self.pin_mode == 'p':
            pin_mode = 'PWM'
            
        self.pin_mode_lbl_var.set(pin_mode)
        
        # if digital input
        if self.pin_type == 'd' and self.pin_mode == 'i':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)
            
        if self.pin_type == 'd' and self.pin_mode == 'o':
            self.pin_state_btn.configure(state = tk.NORMAL)
            
        if self.pin_type == 'a' and self.pin_mode == 'i':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)
        
        if self.pin_type == 'a' and self.pin_mode == 'o':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)
        
        if self.pin_type == 'p' and self.pin_mode == 'o':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)

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

def main():
    
    root = tk.Tk()
    
    root.title("Welcome to LikeGeeks app")
    root.attributes("-topmost", True)
    root.lift()
    
    frame = Frame(root, bg="silver")
    frame.pack(side = "right", fill="y", padx = 5, pady = 5)
  
    # first load configuration for buttons data
    config_obj = JsonConfig('configuration.txt')
    pyfirmata_config_list = config_obj.get_data(True)
    
    print(pyfirmata_config_list)
    
    gui_io_controls = []
    
    # 1. create widgets
    for index in range(len(pyfirmata_config_list)):
        gui_io_controls.append(GUI_IO_control2(root, frame))

    # 1. configure widgets
    for index, pyfirmata_config in enumerate(pyfirmata_config_list):
           gui_io_controls[index].configure(pyfirmata_config)
    
    # lbl = tk.Label(frame, text="Hello")
    # lbl.grid(column=0, row=0)
    
    root.mainloop()
#-----------------------------
if __name__ == "__main__":
    main()