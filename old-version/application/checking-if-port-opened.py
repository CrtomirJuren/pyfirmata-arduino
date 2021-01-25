# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 21:56:44 2021

@author: crtom

# port = serial.Serial(
#     self._arduinoPort,
#     baudrate=9600,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
#     timeout=1
# )
#

# pyfirmata
# self.port = pyfirmata2.Arduino.AUTODETECT
# self.board = pyfirmata2.Arduino(self.port)
"""
import serial
import pyfirmata2
from pyfirmata2 import Arduino

# port = pyfirmata2.Arduino.AUTODETECT
# print(port)
# board = pyfirmata2.Arduino(port)

port = pyfirmata2.Arduino.AUTODETECT    
try:
    print('try')
    print(port)
    board = pyfirmata2.Arduino(port)
    board.digital[2].write(1)
    # if none reserved
except serial.SerialException:
    """
    could not open port 'COM8':
    PermissionError(13, 'Access is denied.', None, 5)
    """
    # serial.Serial("com4", 9600).close()
    # serial.Serial("com8", 57600).close()  
    serial.close() 

    # board = pyfirmata2.Arduino(port)
    # board.digital[2].write(1)
    print('except')

# board.exit()