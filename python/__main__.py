import sys

from math import *
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from src.Lidar import Lidar
from src.Switches import Switches
from src.Container import Container
from src.WebSocketServer import WebSocketServer
from src.ArduinoManager import ArduinoManager
from src.PWMDriver import PWMDriver

import Adafruit_PCA9685
from time import sleep

if __name__ == '__main__':
  container = Container()

  positionWatcher = PositionWatcher()
  positionWatcher.start()
  container.set('positionWatcher', positionWatcher)

  arduinoManager = ArduinoManager(container)
  arduinoManager.identify()
  container.set('arduinoManager', arduinoManager)

  # switches = Switches(container)
  # switches.start()
  # container.set('switches', switches)

  driver = PWMDriver()
  container.set('PWMDriver', driver)

  platform = MotorizedPlatform(container)
  container.set('platform', platform)

  nav = Navigation(container)
  container.set('navigation', nav)

  ws = WebSocketServer(container)
  ws.start()
  container.set('websocket', ws)
  # lidar = Lidar(container)
  # lidar.start()
  # container.set('lidar', lidar)

  def onPos(x, y, t):
    ws.sendData('mainPosition', [x, y, t])

  positionWatcher.setPositionChangedHandler(onPos)

  def app():
    print('READY, all intefaces intialized')
    sleep(1)
    platform.stop()
    # sleep(1)
    # nav.goTo({'x':600, 'y':600, 'orientation':pi })
    while True:
      sleep(100)

  try:
    app()
  except KeyboardInterrupt:
    print("KeyboardInterrupt")
    positionWatcher.stop()
    platform.stop()
    ws.stop()
    switches.stop()
    platform.stop()
    sys.exit()

