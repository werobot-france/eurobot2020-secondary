from adafruit_servokit import ServoKit

import sys

kit = ServoKit(channels=16)
kit.frequency = 50

while True:
    data = input().split(':')
    kit.servo[int(data[0])].angle = int(data[1])