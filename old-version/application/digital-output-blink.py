#!/usr/bin/python3

"""
# Copyright (c) 2012, Fabian Affolter <fabian@affolter-engineering.ch>
# Copyright (c) 2019, Bernd Porr <mail@berndporr.me.uk>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the pyfirmata team nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# The "Hello World" demo how to change a digital port synchronously.
#
# Warning: this is just an example of how to accesss the digital ports.
# For precise timing please use timers or callback handlers
# and not the sleep() command which locks up processing
# and is not precise.
# 
"""

import pyfirmata2
import time
import keyboard

import serial
from pyfirmata2 import Arduino

 
PORT =  pyfirmata2.Arduino.AUTODETECT

# board = Arduino(Arduino.AUTODETECT)
board = pyfirmata2.Arduino(PORT)

# version 1
PIN = 2  # Pin 13 is used
for i in range(10):
    board.digital[PIN].write(1)
    time.sleep(0.2)
    board.digital[PIN].write(0)
    time.sleep(0.2)

# version 2
digital_0 = board.get_pin('d:3:o')
digital_0.write(True)
    
# # close serial port
board.exit()

    
