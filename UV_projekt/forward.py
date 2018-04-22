#!/usr/bin/env python


#This script will make the robot go backwards for a determined amount of time

from __future__ import print_function
from __future__ import division

import time
import brickpi3
import sys
BP = brickpi3.BrickPi3()
duration = sys.argv[1]
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
