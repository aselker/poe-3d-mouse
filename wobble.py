#!/usr/bin/env python

"""
A simple echo server,
to test tcp networking code
"""

import serial
from time import sleep


ser = serial.Serial('/dev/ttyACM0', 9600)#, timeout=0)

while 1:
  for i in list(range(-180,180)) + list(reversed(range(-180,180))):
    reply = (str(i) + ",") * 5 + str(i) + "\n"
    print(reply)
    reply = reply.encode('utf-8')
    ser.write(reply)

    if ser.in_waiting:
      feedback = ser.readline()
      print(feedback.decode('ASCII'))

    sleep(0.01)
