#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from imutils.object_detection import non_max_suppression
from imutils import paths

import time
import brickpi3
import sys
import numpy as np
import imutils
import cv2
import time
import dropbox
import os
# w a s d (movement)
# p + w a s d (camera position)
# snap + name (snapshot with name)
# track + name (tracker with name)

def backward(vrednost):
    BP = brickpi3.BrickPi3()
    duration = float(vrednost)
    duration = duration * 2.5
    # Set the motor speed for all four motors
    speed = 100
    BP.set_motor_power(BP.PORT_A + BP.PORT_B , speed)

    try:
        # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
        print("Encoder A: %6d  B: %6d  C: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C), BP.get_motor_encoder(BP.PORT_D)))
    except IOError as error:
        print(error)
    time.sleep(duration)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

def forward(vrednost):
    BP = brickpi3.BrickPi3()
    duration = float(vrednost)
    duration = duration * 2.5
    # Set the motor speed for all four motors
    speed = -100
    BP.set_motor_power(BP.PORT_A + BP.PORT_B , speed)

    try:
        # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
        print("Encoder A: %6d  B: %6d  C: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C), BP.get_motor_encoder(BP.PORT_D)))
    except IOError as error:
        print(error)
    time.sleep(duration)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

def rotate_left(vrednost):
    BP = brickpi3.BrickPi3()
    duration = float(vrednost)
    duration = duration * 1.25
    #duration = 0.1
    # Set the motor speed for all four motors
    speed = 100
    BP.set_motor_power(BP.PORT_B , -speed)
    BP.set_motor_power(BP.PORT_A , speed)
    try:
        # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
        print("Encoder A: %6d  B: %6d  C: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C), BP.get_motor_encoder(BP.PORT_D)))
    except IOError as error:
        print(error)
    time.sleep(duration)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

def rotate_right(vrednost):
    BP = brickpi3.BrickPi3()
    duration = float(vrednost)
    duration = duration * 1.25
    #duration = 0.1
    # Set the motor speed for all four motors
    speed = -100
    BP.set_motor_power(BP.PORT_A , speed)
    BP.set_motor_power(BP.PORT_B , -speed)
    try:
        # Each of the following BP.get_motor_encoder functions returns the encoder value (what we want to display).
        print("Encoder A: %6d  B: %6d  C: %6d  D: %6d" % (BP.get_motor_encoder(BP.PORT_A), BP.get_motor_encoder(BP.PORT_B), BP.get_motor_encoder(BP.PORT_C), BP.get_motor_encoder(BP.PORT_D)))
    except IOError as error:
        print(error)
    time.sleep(duration)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.


def camera_position(vrednost):
    BP = brickpi3.BrickPi3()
    position = vrednost
    encoder_value = "init"
    if position=="forward":
        encoder_value = 0
    elif position=="backward":
        encoder_value = 180
    elif position=="right":
        encoder_value = 90
    elif position == "left":
        encoder_value = 270
    # Set the motor speed for all four motors
    #speed = -100
    #BP.set_motor_power(BP.PORT_A + BP.PORT_B , speed)
    #BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    BP.set_motor_power(BP.PORT_C, BP.MOTOR_FLOAT)    # float motor D
    BP.set_motor_limits(BP.PORT_C, 30, 100)
    BP.set_motor_position(BP.PORT_C, encoder_value)

    time.sleep(5)
    #time.sleep(duration)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

def snapshot(vrednost):
    argument1 = vrednost
    cam = cv2.VideoCapture(0)
    while True:
        (s, im) = cam.read()
        if s == True:
            cv2.imwrite("images/snapshot_"+argument1+".png",im)
            break
        cam.release
        cam = cv2.VideoCapture(0)
    time.sleep(1)
    cam.release()
    with open('api.txt', 'r') as myfile:
        api = myfile.read().replace('\n', '')
    dbx = dropbox.Dropbox(api)
    with open("images/snapshot_"+argument1+".png", 'rb') as f:
        dbx.files_upload(f.read(), "/drop_images/non_detect_"+argument1+".png")
    time.sleep(3)
    os.remove("images/snapshot_"+argument1+".png")
    print ("success")

def toggle_tracker(vrednost):
    argument1 = vrednost
    with open('api.txt', 'r') as myfile:
        api = myfile.read().replace('\n', '')

    dbx = dropbox.Dropbox(api)

    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # loop over the image paths
    cam = cv2.VideoCapture(0)
    counter_pic = 0
    while True:
        (s, im) = cam.read()
        if s:
            image = imutils.resize(im, width=min(400, im.shape[1]))
            (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                                    padding=(8, 8), scale=1.05)

            if len(rects):
                if rects.any():
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

                    cv2.imwrite("images/snapshot_" + argument1 + ".png", image)
                    with open("images/snapshot_" + argument1 + ".png", 'rb') as f:
                        dbx.files_upload(f.read(), "/drop_images/detect_" + argument1 + str(counter_pic) + ".png")
                    time.sleep(3)
                    os.remove("images/snapshot_" + argument1 + ".png")
                    counter_pic += 1
                    if counter_pic == 20:
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


# w a s d (movement)
# p + w a s d (camera position)
# snap + name (snapshot with name)
# track + name (tracker with name)

while True:
    print("Available commands:")
    print("w a s d (movement)")
    print("p + w a s d (camera position)")
    print("snap + name (snapshot with name)")
    print("track + name (tracker with name)")
	print("Enter your command:")
    text = raw_input("")
    text.split(" ")
    if text[0]=="w":
        forward(0.25)
    elif text[0]=="a":
        rotate_left(0.25)
    elif text[0]=="s":
        backward(0.25)
    elif text[0] == "d":
        rotate_right(0.25)
    elif text[0]=="p":
        if text[1]=="w":
            camera_position("forward")
        elif text[1]=="a":
            camera_position("left")
        elif text[1]=="s":
            camera_position("backward")
        elif text[1] == "d":
            camera_position("right")
    elif text[0] == "snap":
        snapshot(text[1])
    elif text[0]=="track":
        toggle_tracker(text[1])
	print text
