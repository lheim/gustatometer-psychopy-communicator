#!/usr/bin/env python3
import serial
from datetime import datetime
from threading import Lock, Thread, Event

import time

gustato_com = serial.Serial('/dev/cu.wchusbserial1410', baudrate=115200)
print(gustato_com.name)

#print("Sending 'START'")
#gustato_com.write(b'START')

print("Reading ...")
while True:
    current_line = str(gustato_com.readline())
    print(current_line)

print("Exiting trigger thread ...")

print("Sending 'STOP'")
gustato_com.write(b'STOP')
