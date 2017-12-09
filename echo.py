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
    client, address = s.accept()
    print ("Client connected.")
    answer = "Hello!\n"
    b = answer.encode('utf-8')
    client.send(b)

    while 1:
       delim = "\r\n"
       delim = delim.encode('utf-8')
       data = client.recv(size).rstrip( delim)
       data = data.decode('utf-8')
       #print("Data" + data)
       if data:
            if data=="quit":
                client.send("Bye!\n")
                client.close()
                break
            else:
                reply = re.split(',',data[:-1])
               # print(reply)
                try:
                    x = float(reply[0])
                    y = float(reply[1])
                    z = float(reply[2])
                    a = float(reply[3])
                    b = float(reply[4])
                    c = float(reply[5])
                except(ValueError):
                    print("skip")
                data = findAngles(x,y,z,a,b,c)
                data = (str(data)[1:-1])
                #print(data)
                reply = data +  "\n"
                reply = reply.encode('utf-8')
                #print(reply)
                ser.write(reply)

                if ser.in_waiting:
                  feedback = ser.readline()
                  arduinoAngles = feedback.decode('ASCII')
                  meseuredAngles = arduinoAngles[0:-2].split(',')
                  x = float(meseuredAngles[0])
                  y = float(meseuredAngles[1])
                  z = float(meseuredAngles[2])
                  a = float(meseuredAngles[3])
                  b = float(meseuredAngles[4])
                  c = float(meseuredAngles[5])
                  
                  measuredPos = findPosition([x,y,z,a,b,c])
                  print (measuredPos)

                
                
        
                #client.send(reply)
