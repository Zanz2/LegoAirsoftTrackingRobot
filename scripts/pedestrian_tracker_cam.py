# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2
import time
import sys

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over the image paths
cam = cv2.VideoCapture(0)
list_arg = sys.argv
argument1 = list_arg[1]
while True:
    (s, im) = cam.read()
    if s:
        image = imutils.resize(im, width=min(400, im.shape[1]))
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                                padding=(8, 8), scale=1.05)

        if len(rects):
            if rects.any():
                break
        # cv2.imshow("aaa",image)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break
    else:
        cam.release
        cam = cv2.VideoCapture(0)
time.sleep(1)
cam.release()
orig = image.copy()


# draw the original bounding boxes
for (x, y, w, h) in rects:
    cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

# apply non-maxima suppression to the bounding boxes using a
# fairly large overlap threshold to try to maintain overlapping
# boxes that are still people
rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

# draw the final bounding boxes
for (xA, yA, xB, yB) in pick:
    cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

# show some information on the number of bounding boxes
filename = "snapshooty"
print("[INFO] {}: {} original boxes, {} after suppression".format(
    filename, len(rects), len(pick)))

cv2.imwrite("snapshot_"+argument1+".png", image)