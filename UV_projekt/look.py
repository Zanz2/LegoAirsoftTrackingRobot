#!/usr/bin/env python


#This script will make the robot go backwards for a determined amount of time

from __future__ import print_function
from __future__ import division

import time
import brickpi3
import sys
BP = brickpi3.BrickPi3()
position = sys.argv[1]
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

