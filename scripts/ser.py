#!/usr/bin/python3
import cv2
import numpy
import sys
import imutils
import time
import serial
def main():
    ser = serial.Serial('/dev/ttyUSB0',9600)
    time.sleep(2)
    list_arg = sys.argv
    argument1 = list_arg[1]
    argument2 = list_arg[2]
    print(argument1)
    print(argument2)
    if argument1 == "write":
        ser.write(argument2.encode())
        time.sleep(3)
        print("func write")
    if argument1 == "read":
        ser.write("180".encode())
        while 1:
            if ser.inWaiting():
                print(ord((ser.read()).decode()))
                break
        print("func read")
    ser.close()
if __name__ == '__main__':
    main()
