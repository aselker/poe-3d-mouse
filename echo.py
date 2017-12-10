#!/usr/bin/env python

"""
A simple echo server,
to test tcp networking code
"""

import socket
from Listen_angles import*
import re
import serial
import time
import select
ser = serial.Serial('COM19', 115200, timeout=0)



host = ''
port = 50000
backlog = 5
size = 1024
measuredAngles = [1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)


# test = '123456789\r'
# print(test[:-1])

while 1:

  s.setblocking(1)

  client, address = s.accept()
  print ("Client connected.")
  answer = "Hello!\n"
  b = answer.encode('utf-8')
    
  s.setblocking(0)

  measuredPos = "0,0,5,0,0,1"

  while 1:
    delim = "\r\n"
    delim = delim.encode('utf-8')
    try:
      data = client.recv(size).rstrip( delim)
      data = data.decode('utf-8')
    except (BlockingIOError):
      print("Timeout Error")
    #print("Data" + data)
    if data:
      if data=="quit":
        client.send("Bye!\n")
        client.close()
        break
      else:
        reply = re.split(',',data[:-1])

    try:
      (x, y, z, a, b, c) = tuple(float(n) for n in reply)
    except(ValueError):
      print("skip")

    angles = findAngles(x,y,z,a,b,c)
    #print(angles)
    reply = (str(",".join([str(angle) for angle in angles]) + "\n")).encode('utf-8')
    ser.write(reply)

    if ser.in_waiting:
    #  print("Got at least one datum")
      while ser.in_waiting:
     #   print("One more datum")
        feedback = ser.readline()

      arduinoAngles = feedback.decode('utf-8')
      measuredAngles = arduinoAngles[0:-2].split(',') #Remove trailing \n\r
      (x,y,z,a,b,c) = tuple([float(n) for n in measuredAngles])
      
      measuredPos = findPosition([x,y,z,a,b,c])
      measuredPos += "\n"

   # print(measuredPos)
    client.send(measuredPos.encode('utf-8'))
