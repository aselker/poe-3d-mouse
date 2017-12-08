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
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)



host = ''
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
# test = '123456789\r'
# print(test[:-1])

while 1:
    # client, address = s.accept()
    # print ("Client connected.")
    # answer = "Hello!\n"
    # b = answer.encode('utf-8')
    # client.send(b)

    while 1:
       # delim = "\r\n"
       # delim = delim.encode('utf-8')
       # data = client.recv(size).rstrip( delim)
       # data = data.decode('utf-8')
       # #print(data)
       # if data:
       #      if data=="quit":
       #          client.send("Bye!\n")
       #          client.close()
       #          break
       #      else:
       #          reply = re.split(',',data[:-1])
       #         # print(reply)
       #          try:
       #              x = float(reply[0])
       #              y = float(reply[1])
       #              z = float(reply[2])
       #              a = float(reply[3])
       #              b = float(reply[4])
       #              c = float(reply[5])
       #          except(ValueError):
       #              print("skip")
       #          data = findAngles(0,0,4,0,0,1)
       #          data = (str(data)[1:-1])
       #          #print(data)
       #          reply = data + ","
       #          reply = reply.encode('utf-8')
       #          #print(reply)
       #          ser.write(reply)
        feedback = ser.readline()
        print(feedback.decode('ASCII'))
        
                #client.send(reply)
