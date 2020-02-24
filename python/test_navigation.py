# initialize Dualshock interface (in pygame mode or throught node mode)
# initialize Navigation interface

from time import sleep
#from src.dualshock.DualshockThroughtPygame import DualshockThroughtPygame
from src.dualshock.DualshockThroughtNode import DualshockThroughtNode

from src.ControlDispatcher import ControlDispatcher


# servoInterface = None

dualshock = DualshockThroughtNode()
#dualshock = DualshockThroughtPygame()
    
def main():
    controlDispatcher = ControlDispatcher(dualshock)
    
    dualshock.start()
    
    while True:
        sleep(0)



''' 
def mappyt(x, inMin, inMax, outMin, outMax):
    return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

def onAnalog(values):
    print(values)
    
    #dualshock.setLed(mappyt(values['l2'], -1, 1, 0, 255), mappyt(values['rightStickX'], -1, 1, 0, 255), mappyt(values['rightStickY'], -1, 1, 0, 255))
    #dualshock.setRumble(mappyt(values['l2'], -1, 1, 0, 255), mappyt(values['r2'], -1, 1, 0, 255))
    
def onDigital(values):
    print(values)

dualshock.events.on('analog_input', onAnalog)
dualshock.events.on('digital_input', onDigital)


dualshock.start()
'''


try:
    main()
except KeyboardInterrupt:
    navigation.stopAll()
    exit(0)