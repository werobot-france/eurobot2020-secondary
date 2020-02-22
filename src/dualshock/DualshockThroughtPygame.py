from src.dualshock.Dualshock import Dualshock
import pygame
import time

class DualshockThroughtPygame(Dualshock):
    pygame = None

    controllerInitialized = False

    lastControllerActivityClock = 0
    
    def __init__(self):
        super().__init__()
        self.pygame = pygame
        
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
        
    def start(self):
        print('Starting py game controller loop...')
        self.pygame.init()
        self.pygame.joystick.init()
        self.initController()
        time.sleep(2)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == self.pygame.JOYAXISMOTION:
                    newValue = round(event.value, 3)
                    #key = list(self.controllerAnalogValues.keys())[event.axis] 
                    key = self.controllerConfig['analog'][event.axis]
                    if self.controllerAnalogValues[key] != newValue:
                        #print(event.axis, key)
                        # new value detected
                        self.controllerAnalogValues[key] = newValue
                        # dispatch a new event with all the analog values
                        self.events.emit('analog_input', values=self.controllerAnalogValues)
                        
                if event.type == self.pygame.JOYBUTTONDOWN:
                    key = list(self.controllerDigitalValues.keys())[event.button]
                    if self.controllerDigitalValues[key] != True:
                        # new value detected
                        self.controllerDigitalValues[key] = True
                        self.events.emit('digital_input', values=self.controllerDigitalValues)

                elif event.type == self.pygame.JOYBUTTONUP:
                    key = list(self.controllerDigitalValues.keys())[event.button]
                    if self.controllerDigitalValues[key] != False:
                        # new value detected
                        self.controllerDigitalValues[key] = False
                        self.events.emit('digital_input', values=self.controllerDigitalValues)

                elif event.type == self.pygame.JOYHATMOTION:
                    if self.controllerHatValue[event.hat] != event.value:
                        if event.value == (0, 1):
                            self.controllerDigitalValues['up'] = True
                            self.events.emit('digital_input', values=self.controllerDigitalValues)

                        elif event.value == (0, -1):
                            self.controllerDigitalValues['down'] = True
                            self.events.emit('digital_input', values=self.controllerDigitalValues)

                        elif event.value == (1, 0):
                            self.controllerDigitalValues['right'] = True
                            self.events.emit('digital_input', values=self.controllerDigitalValues)

                        elif event.value == (-1, 0):
                            self.controllerDigitalValues['left'] = True
                            self.events.emit('digital_input', values=self.controllerDigitalValues)

                        elif event.value == (0, 0): 
                            self.controllerDigitalValues['up'] = False
                            self.controllerDigitalValues['down'] = False
                            self.controllerDigitalValues['right'] = False
                            self.controllerDigitalValues['left'] = False
                            self.events.emit('digital_input', values=self.controllerDigitalValues)

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


