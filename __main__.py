# initialize Dualshock interface (in pygame mode or throught node mode)
# initialize Navigation interface
''' 
import Adafruit_PCA9685
from src.dualshock.DualshockThroughtPygame import DualshockThroughtPygame
from src.dualshock.DualshockThroughtNode import DualshockThroughtNode
from src.Navigation import Navigation
from src.ControlDispatcher import ControlDispatcher

'''
from src.Stepper import Stepper



# #servoInterface = Adafruit_PCA9685.PCA9685()
# #servoInterface.set_pwm_freq(50)
# servoInterface = None

#dualshock = DualshockThroughtNode()
#dualshock = DualshockThroughtPygame()

# navigation = Navigation(servoInterface)
# controlDispatcher = ControlDispatcher(dualshock, navigation)


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
