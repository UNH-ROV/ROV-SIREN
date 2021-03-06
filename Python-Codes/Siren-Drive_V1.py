"""
UNH ROV 2015/16
Control Code - SIREN

Drive Code V1.0 by Shawn Swist
"""

# ================================================================
#      ----------     Necessary libraries   ------------
from Adafruit_PWM_Servo_Driver import PWM
from ControlFunctions import MotorControl, WriteMotor, Correction

import socket
import sys

from SendReceive import SendReceive

import time     # may not be necessary for final build

# ===================================================================
#    ----------------- Inatilization commands ----------------

# Define the hat over the I2C connection pins
hat = PWM(0x40)

# Set the desired frequency for the servos (50 Hz)
f = 48
hat.setPWMFreq(f)

# Define the thruster pins on the ServoHat
global thruster1
global thruster2
global thruster3
global thruster4
global thruster5
global thruster6

thruster1 = 0;
thruster2 = 2;
thruster3 = 4;
thruster4 = 6;
thruster5 = 8;
thruster6 = 10;
thruster7 = 12;
thruster8 = 14;


center = 307    # Use this to initilize the thrusters


# Add arduino serialport and function to read data
##arduino = serial.Serial('/dev/ttyACM0',115200) # 'serial port',baudrate
##
##def ReadSensor():
##    bytesToRead = arduino.inWaiting()
##    data = arduino.readline(bytesToRead)
##    if data != '':
##        data = int(data)
##    return data

# PC UDP socket built into SendReceive


# Initilize
print "Initilizing ..."
hat.setPWM(thruster1, 0, center)
hat.setPWM(thruster2, 0, center)
hat.setPWM(thruster3, 0, center)
hat.setPWM(thruster4, 0, center)
hat.setPWM(thruster5, 0, center)
hat.setPWM(thruster6, 0, center)
hat.setPWM(thruster7, 0, center)
hat.setPWM(thruster8, 0, center)
# Initilize thrusters for 3 seconds
time.sleep(3)



# ====================================================================
#    ------------------ Main Loop -----------------------

while True:

    # Read pressure and sensor, UDP code works by sending message first
    #pressure = ReadSensor() # temp too ...
    # for inital tests w/o arduino make random numbers to represent pressure
    pressure = 50
    pressure = str(pressure) # Need to send data as a string
    
    # Communication with PC
    # Read in game controller values
    LX,LY,RX,RY,LT,RT = SendReceive(pressure)

    # Use controller values to control thrusters
    MotorControl(RX,RY,LX,LY,RT,LT)

    print LX, LY, RX, RY, LT, RT

    

    # Sital PID controller

    












