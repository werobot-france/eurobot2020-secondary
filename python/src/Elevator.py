#from Stepper import Stepper

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
    clawOpenedPosition = 90
    clawClosedPosition = 180
    
    aboveReefLevel = 100
    takeReefLevel = 50
    lowFairwayLevel = 0
    highFairwayLevel = 30
    supraHighFairwayLevel = 75
    
    '''
    args: {
        'id': Int
        'label': String (name to identify the elevator)
        'clawServoSlot': Int
        'servoInterface': Adafruit_PCA9685.PCA9685 instance
        'arduinoInterface': Arduino instance
    }
    '''
    def __init__(self, **args):
        self.clawServoSlot = args['clawServoSlot']
        self.id = args['id']
        if 'label' in args:
            self.label = args['label']
        if 'servoInterface' in args:
            self.servoInterface = args['servoInterface']
        if 'arduinoInterface' in args:
            self.arduinoInterface = args['arduinoInterface']
            
    def goTo(self, position, speed = 300):
        # WARNING: INVERTED POSITION AND SPEED!
        if position > 0:
            speed = -speed
            position = -position
        
        self.arduinoInterface.sendCommand(
            name = "ELEVATOR_GO_TO",
            params = [self.id, position, speed]
        )
    
    def setClawPosition(self, position):
        if self.servoInterface != None:
            print(position)
            self.servoInterface.set_pwm(self.clawServoSlot, 0, position)
        else:
            print(self.label, 'Set claw position to', position)
        
    def openClaw(self):
        self.setClawPosition(self.clawOpenedPosition)
        
    def closeClaw(self):
        self.setClawPosition(self.clawClosedPosition)
    
    def init(self):
        self.goTo(0)
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