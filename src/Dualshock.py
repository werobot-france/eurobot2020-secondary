import pygame

class Dualshock:
    pygame = None

    controllerInitialized = False

    controllerConfig = {
        'analog': {
            0: 'leftStickX',
            1: 'leftStickY',
            2: 'rightStickX',
            3: 'rightStickY',
            4: 'r2',
            5: 'l2' 
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

    lastControllerActivityClock = 0
    
    
    def __init__(self):
        self.pygame = pygame

    def onControllerAnalog(self):
        #
        print(self.controllerAnalogValues)
        return
    
    def onControllerDigital(self):
        #
        print(self.controllerDigitalValues)
        return
    
    def hasNotController(self):
        self.pygame.joystick.quit()
        self.pygame.joystick.init()
        return self.pygame.joystick.get_count() == 0

    def initController(self):
        if self.hasNotController():
            return False
        else:
            self.pygame.joystick.init()
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            self.setDefaultControllerValues()
            self.controllerInitialized = True
            print('controller was initialized')
            return True

    def setDefaultControllerValues(self):
        for index, analog in enumerate(self.controllerConfig['analog']):
            self.controllerAnalogValues[self.controllerConfig['analog'][index]] = 0.00
        for index, digital in enumerate(self.controllerConfig['digital']):
            self.controllerDigitalValues[self.controllerConfig['digital'][index]] = False
        self.controllerHatValue = [[0, 0]]
        
    def startControllerLoop(self):
        print('Starting py game controller loop...')
        
        self.pygame.joystick.init()
        self.initController()
        while True:
            # Get events   
            for event in pygame.event.get():
                if event.type == self.pygame.JOYAXISMOTION:   
                    newValue = round(event.value, 3)
                    key = list(self.controllerAnalogValues.keys())[event.axis]
                    if self.controllerAnalogValues[key] != newValue:
                        # new value detected
                        self.controllerAnalogValues[key] = newValue
                        self.onControllerAnalog()

                if event.type == self.pygame.JOYBUTTONDOWN:
                    key = list(self.controllerDigitalValues.keys())[event.button]
                    if self.controllerDigitalValues[key] != True:
                        # new value detected
                        self.controllerDigitalValues[key] = True
                        self.onControllerDigital()

                elif event.type == self.pygame.JOYBUTTONUP:
                    key = list(self.controllerDigitalValues.keys())[event.button]
                    if self.controllerDigitalValues[key] != False:
                        # new value detected
                        self.controllerDigitalValues[key] = False
                        self.onControllerDigital()

                elif event.type == self.pygame.JOYHATMOTION:
                    if self.controllerHatValue[event.hat] != event.value:
                        if event.value == (0, 1):
                            self.controllerDigitalValues['up'] = True
                            self.onControllerDigital()

                        elif event.value == (0, -1):
                            self.controllerDigitalValues['down'] = True
                            self.onControllerDigital()

                        elif event.value == (1, 0):
                            self.controllerDigitalValues['right'] = True
                            self.onControllerDigital()

                        elif event.value == (-1, 0):
                            self.controllerDigitalValues['left'] = True
                            self.onControllerDigital()

                        elif event.value == (0, 0): 
                            self.controllerDigitalValues['up'] = False
                            self.controllerDigitalValues['down'] = False
                            self.controllerDigitalValues['right'] = False
                            self.controllerDigitalValues['left'] = False
                            self.onControllerDigital()

                self.lastControllerActivityClock = time.clock()

            # print((time.clock() - self.lastControllerActivityClock))
            if ((time.clock() - self.lastControllerActivityClock) > 3):
                if self.hasNotController() and self.controllerInitialized:
                        print('Controller was disconnected')
                        self.controllerInitialized = False
                elif not(self.hasNotController()) and not(self.controllerInitialized):
                        self.initController()
            clock = self.pygame.time.Clock()
            clock.tick(30)


