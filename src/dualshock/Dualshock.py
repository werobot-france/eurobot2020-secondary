import event_emitter

class Dualshock:
    
    controllerInitialized = False

    controllerConfig = {
        'analog': {
            0: 'leftStickX',
            1: 'leftStickY',
            2: 'l2',
            3: 'rightStickX',
            4: 'rightStickY',
            5: 'r2' 
        },
        'digital': {
            0: 'cross',
            1: 'circle',
            2: 'triangle',
            3: 'square',
            4: 'l1',
            5: 'r1',
            6: 'l2',
            7: 'r2',
            8: 'share',
            9: 'options',
            10: 'ps',
            11: 'leftStick',
            12: 'rightStick',
            13: 'up',
            14: 'down',
            15: 'left',
            16: 'right'
        },
        'hat': 0
    }

    controllerDigitalValues = {}

    controllerAnalogValues = {}
    
    controllerHatValue = [0, 0]

    events = None
    
    def __init__(self):
        self.events = event_emitter.EventEmitter()
        
    def start(self):
        # start loop
        return False
    
    def setLed(self, r, g, b):
        return
    
    def setRumble(self, left, right):
        return

    def setDefaultControllerValues(self):
        for index, analog in enumerate(self.controllerConfig['analog']):
            self.controllerAnalogValues[self.controllerConfig['analog'][index]] = 0.00
        for index, digital in enumerate(self.controllerConfig['digital']):
            self.controllerDigitalValues[self.controllerConfig['digital'][index]] = False
        self.controllerHatValue = [[0, 0]]
        print(self.controllerAnalogValues)
