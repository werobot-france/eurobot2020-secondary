import sys
from math import *
from src.Container import Container
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from time import sleep

container = Container()

positionWatcher = PositionWatcher()
positionWatcher.start()
container.set('positionWatcher', positionWatcher)

def onChange(x, y, theta):
  print(x, y, degrees(theta))

def app():
  positionWatcher.setPositionChangedHandler(onChange)
  positionWatcher.start()

try:
  app()
except KeyboardInterrupt:
  print("\n KeyboardInterrupt")
  positionWatcher.stop()
  sys.exit()

