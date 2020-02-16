# initialize Dualshock interface (in pygame mode or throught node mode)
# initialize Navigation interface

import Adafruit_PCA9685
from src.Dualshock import Dualshock
from src.Navigation import Navigation
from src.ControlDispatcher import ControlDispatcher

servoInterface = Adafruit_PCA9685.PCA9685()
servoInterface.set_pwm_freq(50)

dualshock = Dualshock()
navigation = Navigation(servoInterface)
controlDispatcher = ControlDispatcher(dualshock, navigation)


dualshock.startControllerLoop()