# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 20:57:33 2021

@author: crtom
"""

from pyfirmata2 import Arduino

board = Arduino(Arduino.AUTODETECT)

board.exit()