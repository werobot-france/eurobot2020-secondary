from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class Elevator:
  
  def __init__(self, container):
    i2c = busio.I2C(SCL, SDA)
    self.pca = PCA9685(i2c)
    self.pca.frequency = 50

    self.left  = servo.Servo(self.pca.channels[11])
    self.mid   = servo.Servo(self.pca.channels[10])
    self.right = servo.Servo(self.pca.channels[9])
    
    self.arduino = container.get('arduinoStepper')

  def setClawsAngle(self, angle):
    self.left.angle = 180 - angle
    self.mid.angle = angle
    self.right.angle = angle

  def open(self):
    self.setClawsAngle(90)

  def close(self):
    self.setClawsAngle(90)

  def goTo(self, position, speed):
    self.arduino.sendCommand(
      name = "TWIN_GO_TO",
      params = [position, speed],
      expectResponse = True
    )

  def reset(self, speed = 350):
    self.arduino.sendCommand(
      name = "TWIN_SET_SPEED",
      params = [-speed],
      expectResponse = True
    )
