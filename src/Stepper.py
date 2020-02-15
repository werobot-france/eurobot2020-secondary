from gpiozero import DigitalOutputDevice
import time
import math

class Stepper:
    def __init__(self, dirPin, stepPin, sleepPin = None):
        self.dir =  DigitalOutputDevice(dirPin)
        self.step = DigitalOutputDevice(stepPin)
        if sleepPin != None:
            self.enableOutput = DigitalOutputDevice(sleepPin)
            # by default we disable the card
            self.disable()
        else:
            # if no enable pin is provided we consider the device as always enabled
            self.enableOutput = None
            self.enabled = True
        self.value = 0
        self.scale = 2 * math.pi
        self.minSpeed = 0.002
        self.maxSpeed = 0.0005
        self.isClockwise = None

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

