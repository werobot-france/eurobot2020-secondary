import sys
from math import *
from src.Container import Container
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from time import sleep
from src.ArduinoManager import ArduinoManager
from src.Switches import Switches

container = Container()

arduinoManager = ArduinoManager(container)
arduinoManager.identify()
container.set('arduinoManager', arduinoManager)
  
switches = Switches(container)
switches.start()
container.set('switches', switches)

positionWatcher = PositionWatcher()
positionWatcher.start()
container.set('positionWatcher', positionWatcher)

driver = PWMDriver()
container.set('PWMDriver', driver)

platform = MotorizedPlatform(container)
container.set('platform', platform)

nav = Navigation(container)
container.set('navigation', nav)

nav = Navigation(container)

positionWatcher.start()

def app():  
  platform.stop()
  sleep(0.5)
  
  input('Start ?')
  positionWatcher.reset()
  sleep(0.3)

  nav.goTo({'x': 0, 'y': -200, 'orientation': 3*pi/2, 'stopOn': 'front', 'speed': 20})

try:
  app()
except KeyboardInterrupt:
  print("\n KeyboardInterrupt")
  positionWatcher.stop()
  platform.stop()
  switches.stop()
  sys.exit()

