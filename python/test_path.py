import sys
from math import *
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from src.Container import Container
from src.ArduinoManager import ArduinoManager
from src.Switches import Switches
import Adafruit_PCA9685
from time import sleep

pwm = Adafruit_PCA9685.PCA9685()
platform = MotorizedPlatform(pwm)
positionWatcher = PositionWatcher()

container = Container()
arduinoManager = ArduinoManager(container)
arduinoManager.identify()
switches = Switches(container)

def app():
  platform.stop()
  
  switches.start()
  
  positionWatcher.start()
  print('started position watcher')
  
  container.set('positionWatcher', positionWatcher)
  container.set('platform', platform)
  container.set('switches', switches)

  nav = Navigation(container)

  nav.goToPath([
    #{ 'x': 200, 'y': 900, 'speed': 50, 'orienation': pi },
    { 'x': -200, 'y': 900, 'speed': 20, 'orienation': pi, 'stopOn': 'front' }
  ])

try:
  app()
except KeyboardInterrupt:
  print("KeyboardInterrupt")
  positionWatcher.stop()
  platform.stop()
  switches.stop()
  sys.exit()

