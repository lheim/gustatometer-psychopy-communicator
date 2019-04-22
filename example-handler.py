#!/usr/bin/env python3
import serial

gustatometer = serial.Serial('/dev/cu.wchusbserial1410', baudrate=115200)
print(gustatometer.name)

print("Sending 'START'")
gustatometer.write(b'START')

print("Reading 3 lines ...")
print(gustatometer.readline())
print(gustatometer.readline())
print(gustatometer.readline())

print("Sending 'STOP'")
gustatometer.write(b'STOP')
