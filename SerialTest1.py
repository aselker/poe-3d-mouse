import serial
import time
ser = serial.Serial('COM19', 115200, timeout=0)
var = input("Enter something: ")
var = var.encode('utf-8')
ser.write(var)
while 1:
	var = input("Enter something: ")
	var = var.encode('utf-8')
	ser.write(var)
try:
    print (ser.readline())
    time.sleep(1)
except (TimeoutException):
    print('Data could not be read')