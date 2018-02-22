#!/usr/bin/python
import cv2
import numpy
import sys
import imutils
import time
def main():
	list_arg = sys.argv
	argument1 = list_arg[1]
    cam = cv2.VideoCapture(0)
    while True:
        (s, im) = cam.read()
        if s == True:
            cv2.imwrite("../images/snapshot_"+argument1+".png",im)
            break
        cam.release
        cam = cv2.VideoCapture(0)
    time.sleep(1)
    cam.release()
	with open('api.txt', 'r') as myfile:
    api = myfile.read().replace('\n', '')
	dbx = dropbox.Dropbox(api)
	with open("../images/snapshot_"+argument1+".png", 'rb') as f:
    dbx.files_upload(f.read(), "/drop_images/non_detect_"+argument1+".png")
	time.sleep(3)
	os.remove("../images/snapshot_"+argument1+".png")
    print "success"

if __name__ == '__main__':
    main()
