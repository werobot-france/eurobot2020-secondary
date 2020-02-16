'''
Abstration of navigation
'''
class Navigation:
    escSlots = {
        'frontLeft': 6,
        'frontRight': 5,
        'backLeft': 0,
        'backRight': 1,
        'arm': 2
    }
    
    def __init__(self, servoInterface):
        for slot in self.escSlots:
            # 307 est le signal neutre sous 50 Hz (1.5 / 20 x 4096 = 307)
            self.servoInterface.set_pwm(slot, 0, 307)
        
    # def setPwm(self, arrayLabelValue):
    #     for label, value in arrayLabelValue:
    #         self.servoInterface.set_pwm(self.esc[label], 0, value)
    
    def northTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, a)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['backRight'], 0, a)

    def southTranslation(self, speed):
        self.northTranslation(-speed)

    def eastTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        r = self.convertSpeedToEsc(-speed)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, r)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, r)
        self.servo.set_pwm(self.escSlots['backRight'], 0, a)

    def westTranslation(self, speed):
        self.eastTranslation(- speed)

    def clockwiseRotation(self, speed):
        a = self.convertSpeedToEsc(speed)
        r = self.convertSpeedToEsc(-speed)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, r)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['backRight'], 0, r)

    def antiClockwiseRotation(self, speed):
        self.clockwiseRotation(-speed)

    def northEastTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        s = self.convertSpeedToEsc(0)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, s)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, s)
        self.servo.set_pwm(self.escSlots['backRight'], 0, a)

    def southWestTranslation(self, speed):
        self.northEastTranslation(-speed)

    def northWestTranslation(self, speed):
        a = self.convertSpeedToEsc(speed)
        s = self.convertSpeedToEsc(0)
        self.servo.set_pwm(self.escSlots['frontLeft'], 0, s)
        self.servo.set_pwm(self.escSlots['frontRight'], 0, a)
        self.servo.set_pwm(self.escSlots['backLeft'], 0, a)
        self.servo.set_pwm(self.escSlots['backRight'], 0, s)

    def southEastTranslation(self, speed):
        self.northWestTranslation(-speed)

    def stopAll(self):
        for slot in self.escSlots:
            self.servo.set_pwm(self.escSlots[slot], 0, self.convertSpeedToEsc(0))
