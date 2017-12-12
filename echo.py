#!/usr/bin/env python

"""
A simple echo server,
to test tcp networking code
"""

import socket
from Listen_angles import*
import re
import serial
from time import*
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

def get_arduino():
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
      return measuredPos
def get_unity():
  delim = "\r\n"
  delim = delim.encode('utf-8')
  try:
    data = client.recv(size).rstrip( delim)
    data = data.decode('utf-8')
  except (BlockingIOError):
    print("Timeout Error")

  return data

def set_arduino(data):
  m = 0
  x = 0
  y = 0
  z = 0
  a = 0
  b = 0
  c = 0
  
  if data:
    if data=="quit":
      client.send("Bye!\n")
      client.close()
      
    else:
      reply = re.split(',',data[:-1])
   # print(data);
    
      x = float((reply[0]))
      y = float((reply[1]))
      z = float((reply[2]))
      a = float((reply[3]))
      b = float((reply[4]))
      c = float((reply[5]))
      m = float(reply[6])

    try:  
      angles = findAngles(x, y, z, a, b, c)
      if (len(angles) == 6):
        reply = (str(m) +"," +"%.f"+"," +"%.f"+"," +"%.f"+"," +"%.f"+"," +"%.f"+"," +"%.f" +"\n").encode('utf-8')%(angles[0],angles[1],angles[2],angles[3],angles[4],angles[5])
      else:
        reply = ("0,0,5,0,0,1").encode('utf-8')
      
    except(ValueError):
      print("Got invalid message from Unity" + data)

    print(reply)
    ser.write(reply)

    #print("Data" + data)


# test = '123456789\r'
# print(test[:-1])

while 1:

  s.setblocking(1)

  print ("Ready to connect to client.")
  client, address = s.accept()
  print ("Client connected.")
  answer = "Hello!\n"
  b = answer.encode('utf-8')
    
  s.setblocking(0)

  measuredPos = "0,0,5,0,0,1"
  oldPos = measuredPos
  last = 0

  while 1:
    
    data = get_unity()
    
    oldPos = measuredPos
    before = time()
    measuredPos = get_arduino()
    after = time()
   # print (after-before)
    if not measuredPos:
      measuredPos = oldPos
    current = clock()
    if (current > last + 0.002):
      set_arduino(data)
      last = current

    
    try:
      client.send(measuredPos.encode('utf-8'))
    except(AttributeError):
      print("No measured positions")
   # print(measuredPos)
  # if measuredPos is not None:
  #   oldpos = measuredPos
  #   client.send(measuredPos.encode('utf-8'))
  # else:
  #   client.send(measuredPos.encode('utf-8'))
