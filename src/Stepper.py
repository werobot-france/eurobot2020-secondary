from gpiozero import DigitalOutputDevice
import time
import math

'''
Software-Hardware Inteface for a stepper
'''
class Stepper:
    
    originDirectionIsClockwise = False
    
    value = 0
    scale = 2 * math.pi
    minSpeed = 0.002
    maxSpeed = 0.0005
    isClockwise = None
    
    enableOutput = None
    enabled = True

    '''
    args: {
        'directionPin': Int
        'stepPin': Int
        'sleepPin': Int
        'endSwitchPin': Int
        'originDirectionIsClockwise': Bool
    }
    '''
    def __init__(self, **args):
        # dirPin, stepPin, microSwitchPin, originDirectionIsClockwise = False, sleepPin = None
        self.dir =  DigitalOutputDevice(args['directionPin'])
        self.step = DigitalOutputDevice(args['stepPin'])
        
        if 'endSwitchPin' in args:
            self.endSwitch = DigitalOutputDevice(args['endSwitchPin'])
        
        if 'originDirectionIsClockwise' in args and args['originDirectionIsClockwise']:
            self.originDirectionIsClockwise = True
        
        if 'sleepPin' in args:
            self.enableOutput = DigitalOutputDevice(args['sleepPin'])
            # by default we disable the card
            self.disable()
        # if no enable pin is provided we consider the device as always enabled

    def setScale(self, scale):
        self.scale = scale

    '''
    Referencial for clockwise and anticlockwise
    when the stepper motor pinout is pointed at the top
    '''
    def setClockwise(self):
        self.dir.value = False
        self.isClockwise = True

    def setAnticlockwise(self):
        self.dir.value = True
        self.isClockwise = False

    def getPosition(self):
        return (self.scale*self.value)/200

    def goTo(self, position, speed = 0.8):
        startSpeed = 0.7
        speed = 0.1
        # on fait augementer la vitesse au fur et à mesure sur les 10 steps si la vitesse est sup à 0.7
        for i in range(10):
            self.move(step)

    def computeInterstice(self, speed):
        return self.maxSpeed + (abs(self.minSpeed - self.maxSpeed) * (1-speed))

    '''
    Speed: 1 = Max speeed; 0 = Min speed
    '''
    def move(self, steps, speed = 0.5):
        currentSpeed = speed
        accleratingSteps = steps
        startingSpeed = 4
        if speed > startingSpeed:
            delta = (speed - startingSpeed)/steps
            currentSpeed = startingSpeed
        interstice = self.computeInterstice(currentSpeed)
        for i in range(steps):
            if speed > startingSpeed:
                interstice = self.computeInterstice(startingSpeed + delta*i)
                print(i, interstice)
            self.value += 1
            self.step.value = True
            time.sleep(interstice)
            self.step.value = False
            time.sleep(interstice)

    def fullRotation(self):
        self.move(200)

    def enable(self):
        if self.enableOutput != None:
            self.enableOutput.value = False
            self.enabled = True

    def disable(self):
        if self.enableOutput != None:
            self.enableOutput.value = True
            self.enabled = False

    # 10 steps in the direction of origin until micro switch is closed
    def goToOrigin(self):
        self.enable()
        searchForOrigin = True
        if self.originDirectionIsClockwise:
            self.setClockwise()
        else:
            self.setAnticlockwise()
        while searchForOrigin:
            self.move(10, 0.6)
            if self.endSwitch.value:
                # we reached the end
                searchForOrigin = False
        self.disable()

