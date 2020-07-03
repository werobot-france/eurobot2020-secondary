from time import sleep

'''
Abstration of navigation
'''
class Navigation:
  escSlots = {
    'frontLeft': 15,
    'frontRight': 12, # 12
    'backLeft': 14,
    'backRight': 13 # 13
  }
  servoInterface = None
  
  def __init__(self, servoInterface = None):
    self.servoInterface = servoInterface
    if self.servoInterface != None:
      for slot in self.escSlots:
        # 307 est le signal neutre sous 50 Hz (1.5 / 20 x 4096 = 307)
        self.servoInterface.set_pwm(self.escSlots[slot], 0, 307)
        #self.servoInterface.servo[self.escSlots[slot]] = 307
        #sleep(0)
    else:
      print('> NAVIGATION IS MOCKED')
      
  def setPwm(self, arrayLabelValue):
    #print(arrayLabelValue)
    if self.servoInterface != None:
      for label in arrayLabelValue:
        self.servoInterface.set_pwm(self.escSlots[label], 0, arrayLabelValue[label])
        #self.servoInterface.servo[self.escSlots[label]] = 307
        #sleep(0)
    else:
      print(arrayLabelValue)

  # équivalent de la fonction map() de arduino
  def mappyt(self, x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
  
  # fonction esc pour une vitesse de moteur de -100 à 100()
  def convertSpeedToEsc(self, speed):
    return round(self.mappyt(speed, 0, 100, 307, 410))
  
  def eastTranslation(self, speed):
    a = self.convertSpeedToEsc(speed)
    self.setPwm({
        'frontLeft': a,
        'frontRight': a,
        'backLeft': a,
        'backRight': a
    })
    # self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
    # self.servo.set_pwm(self.escSlots['frontRight'], 0, a)
    # self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
    # self.servo.set_pwm(self.escSlots['backRight'], 0, a)

  def southTranslation(self, speed):
    self.northTranslation(-speed)

  def northTranslation(self, speed):
    a = self.convertSpeedToEsc(speed)
    r = self.convertSpeedToEsc(-speed)
    self.setPwm({
        'frontLeft': a,
        'frontRight': r,
        'backLeft': r,
        'backRight': a
    })
    # self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
    # self.servo.set_pwm(self.escSlots['frontRight'], 0, r)
    # self.servo.set_pwm(self.escSlots['backLeft'], 0, r)
    # self.servo.set_pwm(self.escSlots['backRight'], 0, a)

  def westTranslation(self, speed):
    self.eastTranslation(- speed)

  def clockwiseRotation(self, speed):
    a = self.convertSpeedToEsc(speed)
    r = self.convertSpeedToEsc(-speed)
    self.setPwm({
        'frontLeft': a,
        'frontRight': a,
        'backLeft': r,
        'backRight': r
    })
    # self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
    # self.servo.set_pwm(self.escSlots['frontRight'], 0, r)
    # self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
    # self.servo.set_pwm(self.escSlots['backRight'], 0, r)

  def antiClockwiseRotation(self, speed):
    self.clockwiseRotation(-speed)

  def northEastTranslation(self, speed):
    a = self.convertSpeedToEsc(speed)
    s = self.convertSpeedToEsc(0)
    self.setPwm({
        'frontLeft': a,
        'frontRight': s,
        'backLeft': s,
        'backRight': a
    })
    # self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
    # self.servo.set_pwm(self.escSlots['frontRight'], 0, s)
    # self.servo.set_pwm(self.escSlots['backLeft'], 0, s)
    # self.servo.set_pwm(self.escSlots['backRight'], 0, a)

  def southWestTranslation(self, speed):
    self.northEastTranslation(-speed)

  def northWestTranslation(self, speed):
    a = self.convertSpeedToEsc(speed)
    s = self.convertSpeedToEsc(0)
    self.setPwm({
        'frontLeft': s,
        'frontRight': a,
        'backLeft': a,
        'backRight': s
    })
    # self.servo.set_pwm(self.escSlots['frontLeft'], 0, s)
    # self.servo.set_pwm(self.escSlots['frontRight'], 0, a)
    # self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
    # self.servo.set_pwm(self.escSlots['backRight'], 0, s)

  def southEastTranslation(self, speed):
    self.northWestTranslation(-speed)

  def stopAll(self):
    #print('STOP ALL')
    speed = self.convertSpeedToEsc(0)
    self.setPwm({
      'frontLeft': speed,
      'frontRight': speed,
      'backLeft': speed,
      'backRight': speed
    })
    #self.servo.set_pwm(self.escSlots[slot], 0, self.convertSpeedToEsc(0))

  def callSmth(self, speed = 410):
    self.setPwm({
      'frontLeft': self.convertSpeedToEsc(0),
      'frontRight': self.convertSpeedToEsc(0),
      'backLeft': 410,
      'backRight': self.convertSpeedToEsc(0)
    })
  
  def  