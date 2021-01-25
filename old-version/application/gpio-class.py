# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:51:15 2021

@author: crtjur
"""
# from tkinter import *
import tkinter as tk

# class GPIO(tk.Frame):
#     """Each GPIO class draws a Tkinter frame containing:
#     - A Label to show the GPIO Port Name
#     - A data direction spin box to select pin as input or output
#     - A checkbox to set an output pin on or off
#     - An LED widget to show the pin's current state
#     - A Label to indicate the GPIOs current function"""
#     gpio_modes = ("Passive","Input","Output")

#     def __init__(self,parent,pin=0,name=None,**kw):
#       self.pin = pin
#       if name == None:
#           self.name = "GPIO %02d" % (self.pin)
#           tk.Frame.__init__(self,parent,width=150,height=20,relief=tk.SUNKEN,bd=1,padx=5,pady=5)
#           ##Future capability
#           ##self.bind('<Double-Button-1>', lambda e, s=self: self._configurePin(e.y))
#           self.parent = parent
#           # self.configure(**kw)
#           self.state = False
#           self.cmdState = tk.IntVar()
#           self.Label = tk.Label(self,text=self.name)
#           # # self.mode_sel = tk.Spinbox(self,values=gpio_modes,wrap=True,command=self.setMode)
#           # self.mode_sel = tk.Spinbox(self,values=gpio_modes,wrap=True)
#           # self.set_state = tk.Checkbutton(self,text="High/Low",variable=self.cmdState,command=self.toggleCmdState)
#           # self.led = LED(self,20)
#           self.Label.grid(column=0,row=0)
#           # self.mode_sel.grid(column=1,row=0)
#           # self.set_state.grid(column=2,row=0)
#           # self.current_mode = StringVar()
#            # self.led.grid(column=3,row=0)

#           # self.set_state.config(state=DISABLED)
#           # function = self.getPinFunctionName()
#           # if function not in ['Input','Output']:
#           #   self.mode_sel.delete(0,'end')
#           #   self.mode_sel.insert(0,function)
#           #   self.mode_sel['state'] = DISABLED


        
class digitalPin(tk.Frame, number):
    def __init__(self, frame):
        self.Label = tk.Label(frame, text=number)
        self.Label.grid(column=0,row=0)
    
    def set_state(self):
        pass
    
    def get_state(self):
        pass


# create tkinter window
root = tk.Tk()
root.title("Welcome to LikeGeeks app")
root.geometry('460x350')

# create all of the main containers
header_frame = tk.Frame(root, bg='grey', width=450, height=50, pady=3)
top_frame = tk.Frame(root, bg='grey', width=450, height=50, pady=3)
center = tk.Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
btm_frame = tk.Frame(root, bg='white', width=450, height=45, pady=3)
btm_frame2 = tk.Frame(root, bg='lavender', width=450, height=60, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

header_frame.grid(row=0, sticky="ew")
top_frame.grid(row=1, sticky="ew")
center.grid(row=2, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")
btm_frame2.grid(row=4, sticky="ew")

gpio_mode = ('input', 'output')
gpio_type = ('digital', 'PWM', 'analog')


# create digital pins 2-14
for i in range(2,14):
    gpio_frame = tk.Frame(top_frame, bg='white', pady=3, highlightbackground="black", highlightthickness=1)
    gpio_frame.grid(row=i, sticky="ew")
    # headers
    if not i:
        tk.Label(gpio_frame, text='PIN N', width = 5).grid(row=i, column = 0) #, bg = 'grey'
        tk.Label(gpio_frame, text='MODE', width = 10).grid(row=i, column = 1)
        tk.Label(gpio_frame, text='TYPE', width = 10).grid(row=i, column = 2)
        tk.Label(gpio_frame, text='STATUS', width = 10).grid(row=i, column = 3)
        tk.Label(gpio_frame, text='VALUE', width = 10).grid(row=i, column = 4) 
        print('asd')
    else:
        # create the widgets for the top frame
        pin_text = str(i)
        pin_label = tk.Label(gpio_frame, text=pin_text, width = 5)
        mode_sel = tk.Spinbox(gpio_frame, width = 10, values = gpio_mode, wrap=True)
        type_sel = tk.Spinbox(gpio_frame,width = 10, values = gpio_type, wrap=True)
        button_label = tk.Button(gpio_frame,width = 10) #height = 100,
        value = tk.Entry(gpio_frame,background="pink", width = 10)
    
        # layout the widgets in the top frame
        pin_label.grid(row=i, column = 0) # columnspan=1
        mode_sel.grid(row=i, column = 1)
        type_sel.grid(row=i, column = 2)
        button_label.grid(row=i, column = 3)
        value.grid(row=i, column=4)
        # entry_L.grid(row=1, column=3)

gpio_frame = tk.Frame(top_frame, bg='white', pady=3, highlightbackground="black", highlightthickness=1)
gpio_frame.grid(row=i, sticky="ew")
pin = digitalPin(gpio_frame, number =i)
    
# main loop
root.mainloop()