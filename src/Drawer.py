from Stepper import Stepper
from time import sleep

'''
Drawer include:
- interface to control the drawer (opened/closed)
- interface to control the squeezer (opened/closed)
'''
class Drawer:
    
    servoInterface = None
    
    squeezerOpenedPosition = 0
    squeezerClosedPosition = 180
    
    closedPosition = 0
    openedPosition = 0

    '''
    args: {
        'squeezerServoSlot': Int
        'stepperConfig': StepperConfig (see Stepper.py __init__())
        'servoInteface': Adafruit_PCA9685.PCA9685 instance
    }
    '''
    def __init__(self, **args):
        self.squeezerServoSlot = args['squeezerServoSlot']
        if 'servoInterface' in args:
            self.servoInterface = args['servoInteface']
        '''
        directionPin = args['directionPin'],
        stepPin = args['stepPin'],
        sleepPin = args['sleepPin'],
        endSwitchPin = args['endSwitchPin'],
        originDirectionIsClockwise = args['originDirectionIsClockwise']
        '''
        self.stepper = Stepper(args['stepperConfig'])
    
    def setSqueezerPosition(self, position):
        if self.servoInterface != None:
            self.servoInteface.set_pwm(self.squeezerServoSlot, 0, position)
        else:
            print(self.label, 'Set squeezer position to', position)
        
    def squeeze(self):
        self.setSqueezerPosition(self.squeezerOpenedPosition)
        
    def unSqueeze(self):
        self.setSqueezerPosition(self.squeezerClosedPosition)
        
    def init(self):
        self.squeeze()
        sleep(4)
        self.stepper.goToOrigin()