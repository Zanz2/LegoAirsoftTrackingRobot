import cv2
import time
import numpy
import sys
def main():
    cam = cv2.VideoCapture(0)
    s, im = cam.read()
    time.sleep(4)
    cam.release() 
    cv2.destroyAllWindows()
    cv2.imwrite("../images/snapshot_1.png",im)
    throw_away()
    
def throw_away():
    cam = cv2.VideoCapture(0)
    s, im = cam.read()
    time.sleep(4)
    cam.release() 
    cv2.destroyAllWindows()
    cv2.imwrite("../images/snapshot_2.png",im)

if __name__ == '__main__':
    main()
