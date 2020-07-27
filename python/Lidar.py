from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class Lidar:
  
  def __init__(self, container):
    i2c = busio.I2C(SCL, SDA)
    self.pca = PCA9685(i2c)
    self.pca.frequency = 50

    self.servo = servo.Servo(self.pca.channels[7])

  def balayage(self):
    while True:
      self.servo.angle = 180
      self.servo.angle = 0


#  def setClawsAngle(self, angle):
#    self.left.angle = 180 - angle
#    self.mid.angle = angle
#    self.right.angle = angle
#
#  def setClawAngle(self, index, angle):
#    if index == 0:
#        self.right.angle = angle
#    if index == 1:
#        self.mid.angle = angle
#    if index == 2:
#        self.left.angle = 180 - angle
