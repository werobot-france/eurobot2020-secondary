from Adafruit_PCA9685 import PCA9685

class PWMDriver:
  def __init__(self):
    self.driver = PCA9685()
    self.driver.set_pwm_freq(50)
  
  def setAngle(self, slot, angle):
    self.driver.set_pwm(slot, 0, int(mappyt(angle, 0, 180, 75, 510)))

  def setPwm(self, slot, off, on):
    self.driver.set_pwm(slot, off, on)

  def mappyt(self, x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
