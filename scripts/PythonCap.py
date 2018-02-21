#!/usr/bin/python
import cv2
import numpy
import sys
import imutils
import time
def main():
    cam = cv2.VideoCapture(0)
    while True:
        (s, im) = cam.read()
        if s == True:
            cv2.imwrite("../images/snapshot_1.png",im)
            break
        cam.release
        cam = cv2.VideoCapture(0)
    time.sleep(1)
    cam.release()
    print "success"

if __name__ == '__main__':
    main()
