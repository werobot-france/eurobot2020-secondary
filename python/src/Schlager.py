from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class Schlager:
  
  def __init__(self, container):
    i2c = busio.I2C(SCL, SDA)
    self.pca = PCA9685(i2c)
    self.pca.frequency = 50
    self.servo = servo.Servo(self.pca.channels[8])

  def open(self, selector = None):
    self.servo.angle = 180

  def close(self, selector = None):
    self.servo.angle = 55
