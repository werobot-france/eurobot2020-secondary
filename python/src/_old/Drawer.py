from time import sleep

'''
Drawer include:
- interface to control the drawer (opened/closed)
- interface to control the squeezer (opened/closed)
'''
class Drawer:
    
    servoInterface = None
    
    squeezerOpenedPosition = 90
    squeezerClosedPosition = 180
    
    '''
    args: {
        'squeezerServoSlot': Int
        'servoInteface': Adafruit_PCA9685.PCA9685 instance
        'arduinoInterface': Arduino instance
    }
    '''
    def __init__(self, **args):
        self.squeezerServoSlot = args['squeezerServoSlot']
        if 'servoInterface' in args:
            self.servoInterface = args['servoInterface']
        if 'arduinoInterface' in args:
            self.arduinoInterface = args['arduinoInterface']
            
    def close(self):
        self.arduinoInterface.sendCommand(
            name = 'DRAWER_GO_TO_BACK',
            params = [],
            expectResponse = True
        )
        
    def open(self):
        self.arduinoInterface.sendCommand(
            name = 'DRAWER_GO_TO_FRONT',
            params = [],
            expectResponse = True
        )
    
    def setSqueezerPosition(self, position):
        if self.servoInterface != None:
            #self.servoInterface.set_pwm(self.squeezerServoSlot, 0, position)
            #kit.servo[self.squeezerServoSlot].angle = position
            self.servoInterface.setAngle(self.squeezerServoSlot, position)
            print('Set squeezer position to', position, 'in slot', self.squeezerServoSlot)
        else:
            print(self.label, 'Set squeezer position to', position)
        
    def squeeze(self):
        self.setSqueezerPosition(self.squeezerOpenedPosition)
        
    def unSqueeze(self):
        self.setSqueezerPosition(self.squeezerClosedPosition)
        
    def init(self):
        self.squeeze()
        sleep(4)
        self.close()