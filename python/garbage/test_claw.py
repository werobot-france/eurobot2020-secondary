
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)
pca.frequency = 50

left = servo.Servo(pca.channels[11])
mid = servo.Servo(pca.channels[10])
right = servo.Servo(pca.channels[9])

openPos = 120
closePos = 90

def setAngle(angle):
  left.angle = 180 - angle
  mid.angle = angle
  right.angle = angle

