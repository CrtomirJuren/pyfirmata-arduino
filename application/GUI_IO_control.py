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

import pyfirmata2
from pyfirmata2 import Arduino

class GUI_IO_control(tk.Frame):
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
        self.control_variant = None
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
            if not self.simulated:
                self.pin_class.write(False)
        else:
            self.pin_state_btn.configure(text="High", relief=tk.RAISED)
            # self.lbl.configure(text="  OFF ", bg="red")
            if not self.simulated:
                self.pin_class.write(True)

    def configure(self, pyfirmata_config):

        # translate pyfirmata_config to readable
        self.pin_type = pyfirmata_config.split(':')[0]
        self.pin_number = pyfirmata_config.split(':')[1]
        self.pin_mode = pyfirmata_config.split(':')[2]

        if self.pin_type == 'd' and self.pin_mode == 'i':
            self.control_variant = 'digital_input'
        if self.pin_type == 'd' and self.pin_mode == 'o':
            self.control_variant = 'digital_output'
        if self.pin_type == 'a' and self.pin_mode == 'i':
            self.control_variant = 'analog_input'
        if self.pin_type == 'a' and self.pin_mode == 'o':
            self.control_variant = 'analog_output'
        if self.pin_type == 'p' and self.pin_mode == 'o':
            self.control_variant = 'pwm_output'

        # Button has three states : active, normal, disabled
        # configure label
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
        if self.control_variant == 'digital_input':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)

        if self.control_variant == 'digital_output':
            #enable button
            self.pin_state_btn.configure(state = tk.NORMAL)
            pass

        if self.control_variant == 'analog_input':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)
            pass

        if self.control_variant == 'analog_output':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)
            pass

        if self.control_variant == 'pwm_output':
            #disable button
            self.pin_state_btn.configure(text="")
            self.pin_state_btn.configure(state = tk.DISABLED)
            pass

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


class DigitalOutput():
    def __init__(self, parent, frame, board, pin_type, pin_number, pin_mode, simulated, *args, **kwargs):

        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = frame

        self.pin_type = pin_type
        self.pin_number = pin_number
        self.pin_mode = pin_mode
        self.simulated = simulated
      
        # pyfirmata create pin
        self.board = board
        pyfirmata_pin_config = pin_type+':'+pin_number+':'+pin_mode

        # pin number: label
        self.pin_number_lbl = tk.Label(self.frame, width = 5, text = self.pin_number)
        self.pin_mode_lbl = tk.Label(self.frame, width = 5, text = 'DO')  # without text and textvariable
        # output control: button
        self.pin_state_btn = tk.Button(self.frame, text="Off", relief=tk.RAISED, width = 5, command=self.clicked)

        # grid
        self.pin_number_lbl.grid(row=0,column=0)
        self.pin_mode_lbl.grid(row=0,column=1)
        self.pin_state_btn.grid(row=0,column=2)
        
        # initialize pyfirmata
        if not simulated:
            self.pin_class =  self.board.get_pin(pyfirmata_pin_config)

    def destroy(self):
        # destroy widgets in frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # destroy frame
        self.frame.destroy()
    
    def clicked(self):
        if self.pin_state_btn['text'] == "On":
            self.pin_state_btn.configure(text="Off", relief=tk.RAISED)
            # self.lbl.configure(text="  ON  ", bg="green")
            if not self.simulated:
                self.pin_class.write(False)
        else:
            self.pin_state_btn.configure(text="On", relief=tk.SUNKEN)
            # self.lbl.configure(text="  OFF ", bg="red")
            if not self.simulated:
                self.pin_class.write(True)

    def read(self):
        pass
    
    def write(self):
        pass

class DigitalInput():
    def __init__(self, parent, frame, board, pin_type, pin_number, pin_mode, simulated, *args, **kwargs):

        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = frame

         # pyfirmata create pin
        self.board = board
        pyfirmata_pin_config = pin_type+':'+pin_number+':'+pin_mode
  
        self.pin_type = pin_type
        self.pin_number = pin_number
        self.pin_mode = pin_mode
        self.simulated = simulated        
        # pin number: label
        self.pin_number_lbl = tk.Label(self.frame, width = 5, text = self.pin_number)
        self.pin_mode_lbl = tk.Label(self.frame, width = 5, text = 'DI')  # without text and textvariable
        # digital input led: canvas
        self.led = tk.Canvas(self.frame, height=20, width=20)
        self.led.create_oval(5,5,20,20, fill='white', tags="led")

        # grid
        self.pin_number_lbl.grid(row=0,column=0)
        self.pin_mode_lbl.grid(row=0,column=1)
        self.led.grid(row=0,column=2)
    
        # initialize pyfirmata
        if not simulated:
            self.pin_class =  self.board.get_pin(pyfirmata_pin_config)

    
    def destroy(self):
        # destroy widgets in frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # destroy frame
        self.frame.destroy()
    
    def clicked(self):
        pass

    def read(self):
        if not self.simulated:
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
    
    def write(self):
        pass            
    
class AnalogInput():
    def __init__(self, parent, frame, board, pin_type, pin_number, pin_mode, simulated, *args, **kwargs):

        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = frame

         # pyfirmata create pin
        self.board = board
        pyfirmata_pin_config = pin_type+':'+pin_number+':'+pin_mode

        self.pin_type = pin_type
        self.pin_number = pin_number
        self.pin_mode = pin_mode
        self.simulated = simulated        
        
        #Output Floats on right Side
        self.value_var = tk.DoubleVar()
        self.value_var.set('_.__')

        # pin number: label
        self.pin_number_lbl = tk.Label(self.frame, width = 5, text = self.pin_number)
        self.pin_mode_lbl = tk.Label(self.frame, width = 5, text = 'AI')  # without text and textvariable

        self.entry = tk.Entry(self.frame, width = 5, bd =5, state='disabled', textvariable=self.value_var)
        self.unit_lbl = tk.Label(self.frame, width = 5, text = '[V]')

        # grid
        self.pin_number_lbl.grid(row=0,column=0)
        self.pin_mode_lbl.grid(row=0,column=1)
        self.entry.grid(row=0,column=2)
        self.unit_lbl.grid(row=0,column=3)
    
        # initialize pyfirmata
        if not simulated:
            self.pin_class =  self.board.get_pin(pyfirmata_pin_config)

    
    def destroy(self):
        # destroy widgets in frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # destroy frame
        self.frame.destroy()
    
    def clicked(self):
        pass
    
    def read(self):
        if not self.simulated:
            analog_value = self.pin_class.read()
        else:
            analog_value = random.uniform(9, 10.0)
            # print(self.pin_class.read())
            display = "{:.4f}".format(analog_value)
            self.string_var.set(display)

class AnalogOutput():
    def __init__(self, parent, frame, board, pin_type, pin_number, pin_mode, simulated, *args, **kwargs):

        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = frame

        # pyfirmata create pin
        self.board = board
        pyfirmata_pin_config = pin_type+':'+pin_number+':'+pin_mode
    
        self.pin_type = pin_type
        self.pin_number = pin_number
        self.pin_mode = pin_mode
        self.simulated = simulated        
        #Output Floats on right Side
        self.value_var = tk.DoubleVar()
        self.value_var.set('_.__')

        # pin number: label
        self.pin_number_lbl = tk.Label(self.frame, width = 5, text = self.pin_number)
        self.pin_mode_lbl = tk.Label(self.frame, width = 5, text = 'AO')  # without text and textvariable

        self.entry = tk.Entry(self.frame, width = 5, bd =5, textvariable=self.value_var)
        self.unit_lbl = tk.Label(self.frame, width = 5, text = '[V]')
        self.pin_state_btn = tk.Button(self.frame, text="Disabled", relief=tk.RAISED, width = 10, command=self.clicked)


        # grid
        self.pin_number_lbl.grid(row=0,column=0)
        self.pin_mode_lbl.grid(row=0,column=1)
        self.entry.grid(row=0,column=2)
        self.unit_lbl.grid(row=0,column=3)
        self.pin_state_btn.grid(row=0,column=4)

        # initialize pyfirmata
        if not simulated:
            self.pin_class =  self.board.get_pin(pyfirmata_pin_config)

    
    def destroy(self):
        # destroy widgets in frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # destroy frame
        self.frame.destroy()
    
    def clicked(self):
        if self.pin_state_btn['text'] == "Enabled":
            self.pin_state_btn.configure(text="Disabled", relief=tk.RAISED)
            # self.lbl.configure(text="  ON  ", bg="green")
            if not self.simulated:
                pass
        else:
            self.pin_state_btn.configure(text="Enabled", relief=tk.SUNKEN)
            # self.lbl.configure(text="  OFF ", bg="red")
            if not self.simulated:
                pass

    def read(self):
        pass

    def write(self):
        pass

class PWMOutput():
    def __init__(self, parent, frame, board, pin_type, pin_number, pin_mode, simulated, *args, **kwargs):

        # tk.Frame.__init__(self, parent)
        self.parent = parent
        self.frame = frame

        # pyfirmata create pin
        self.board = board
        pyfirmata_pin_config = pin_type+':'+pin_number+':'+pin_mode

        self.pin_type = pin_type
        self.pin_number = pin_number
        self.pin_mode = pin_mode
        self.simulated = simulated     
        
        self.value_var = tk.IntVar()
        self.value_var.set('___')
        
        # pin number: label
        self.pin_number_lbl = tk.Label(self.frame, width = 5, text = self.pin_number)
        self.pin_mode_lbl = tk.Label(self.frame, width = 5, text = 'PWM')  # without text and textvariable
        self.entry = tk.Entry(self.frame, width = 5, bd =5, textvariable=self.value_var)
        self.unit_lbl = tk.Label(self.frame, width = 5, text = '[%]')

        self.pin_state_btn = tk.Button(self.frame, text="Disabled", relief=tk.SUNKEN, width = 5, command=self.clicked)

        # grid
        self.pin_number_lbl.grid(row=0,column=0)
        self.pin_mode_lbl.grid(row=0,column=1)
        self.pin_state_btn.grid(row=0,column=3)

        # initialize pyfirmata
        if not simulated:
            self.pin_class =  self.board.get_pin(pyfirmata_pin_config)
      
        
    def destroy(self):
        # destroy widgets in frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # destroy frame
        self.frame.destroy()
    
    def clicked(self):
        if self.pin_state_btn['text'] == "Enabled":
            self.pin_state_btn.configure(text="Disabled", relief=tk.SUNKEN)
            # self.lbl.configure(text="  ON  ", bg="green")
            if not self.simulated:
                pass
        else:
            self.pin_state_btn.configure(text="Enabled", relief=tk.RAISED)
            # self.lbl.configure(text="  OFF ", bg="red")
            if not self.simulated:
                pass
            
    def read(self):
        pass
    
    def write(self):
        pass
    
io_controls = []

def delete_frames():
    global io_controls    
    control = io_controls.pop()
    control.destroy()

def main():
    global io_controls 
    simulated = True
    
    root = tk.Tk()

    root.title("app")
    root.attributes("-topmost", True)
    root.lift()

    button = tk.Button(root, text="Press to Delete frames", command=delete_frames)
    button.pack()

    # first load configuration for buttons data
    config_obj = JsonConfig('configuration.txt')
    pyfirmata_config_list = config_obj.get_data(True)
    board = None
    
    # if not simulated:
    #     port = pyfirmata2.Arduino.AUTODETECT
    #     print("Setting up the connection to the board ...")
    #     board = pyfirmata2.Arduino(port)
    #     # enable arduino sampling --> for inputs
    #     # self.board.samplingOn()
        
    # 1. configure widgets
    for index, pyfirmata_config in enumerate(pyfirmata_config_list):
        frame = tk.Frame(root, bg="silver")
        # frame.pack(fill="x", padx = 5, pady = 5) #side = "right", 
        frame.pack(fill= tk.BOTH, padx = 5, pady = 5) #side = "right", 

        pin_type = pyfirmata_config.split(':')[0]
        pin_number = pyfirmata_config.split(':')[1]
        pin_mode = pyfirmata_config.split(':')[2]
        
        
        # digital_input'
        if pin_type == 'd' and pin_mode == 'i':
            control = DigitalInput(root, frame, board, pin_type, pin_number, pin_mode, simulated)
        #'digital_output'
        if pin_type == 'd' and pin_mode == 'o':
            control = DigitalOutput(root, frame, board, pin_type, pin_number, pin_mode, simulated)
        # 'analog_input'    
        if pin_type == 'a' and pin_mode == 'i':
            control = AnalogInput(root, frame, board, pin_type, pin_number, pin_mode, simulated)
        # 'analog_output'
        if pin_type == 'a' and pin_mode == 'o':
            control = AnalogOutput(root, frame, board, pin_type, pin_number, pin_mode, simulated)
        # 'pwm_output'    
        if pin_type == 'p' and pin_mode == 'o': 
            control = PWMOutput(root, frame, board, pin_type, pin_number, pin_mode, simulated)
        
        io_controls.append(control)
        
    root.mainloop()
#-----------------------------
if __name__ == "__main__":
    main()