from Stepper import Stepper

'''
Elevator include:
- interface to control the level using the stepper motor
- interface to control the claw (open/close position)
'''
class Elevator:
    servoInterface = None
    label = 'NO_LABEL'
    stepper = None
    
    # in degrees
    clawOpenedPosition = 0
    clawClosedPosition = 180
    
    aboveReefLevel = 100
    takeReefLevel = 50
    lowFairwayLevel = 0
    highFairwayLevel = 30
    supraHighFairwayLevel = 75
    
    '''
    args: {
        'label': String (name to identify the elevator)
        'clawServoSlot': Int
        'stepperConfig': StepperConfig (see Stepper.py __init__())
        'servoInteface': Adafruit_PCA9685.PCA9685 instance
    }
    '''
    def __init__(self, **args):
        self.clawServoSlot = args['clawServoSlot']
        if 'label' in args:
            self.label = args['label']
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
        
    def setClawPosition(self, position):
        if self.servoInterface != None:
            self.servoInteface.set_pwm(self.clawServoSlot, 0, position)
        else:
            print(self.label, 'Set claw position to', position)
        
    def openClaw(self):
        self.setClawPosition(self.clawOpenedPosition)
        
    def closeClaw(self):
        self.setClawPosition(self.clawClosedPosition)
    
    def init(self):
        self.stepper.goToOrigin()
        self.closeClaw()
        
    def takeBuoyInReefRoutine(self):
        '''
        - si il est pas au bon niveau, se mettre au niveau haut
        - ouvrir pince
        - descendre au niveau eceuil
        - fermer pince
        - se mettre au niveau haut
        '''
        return
    
    def dispenseBuoyRoutine(self):
        '''
        - s'il il n'est pas ouvert, ouvrir le tiroir
        - s'il il est pas au bon niveau, se mettre au niveau depiller bas
        - ouvrir pince
        - se mettre au niveau depiller haut
        - fermer pince
        - fermer squeezer
        - se mettre au niveau deplier supra haut
        - ouvrir squeezer
        - (ranger tiroir)
        '''
        return