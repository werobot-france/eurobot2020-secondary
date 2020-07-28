from src.Elevator import Elevator
from src.Container import Container
from src.ArduinoManager import ArduinoManager
from src.Arduino import Arduino

container = Container()
a = ArduinoManager(container)
a.identify()

# print(container.get('arduinoStepper'))
# print(container.get('arduinoSwitches'))

elevator = Elevator(container)

elevator.reset()

# e.goTo(750, 500)

print('READY!')
