import sys
from math import *
from src.Container import Container
from src.Game import Game
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Navigation import Navigation
from src.PositionWatcher import PositionWatcher
from src.Lidar import Lidar
from src.Switches import Switches
from src.WebSocketServer import WebSocketServer
from src.ArduinoManager import ArduinoManager
from src.Scripts import Scripts
from time import sleep

if __name__ == '__main__':
  container = Container()
  
  ws = WebSocketServer(container)
  container.set('websocket', ws)

  game = Game(container)
  container.set('game', game)
  
  positionWatcher = PositionWatcher()
  #positionWatcher.start()
  container.set('positionWatcher', positionWatcher)

  arduinoManager = ArduinoManager(container)
  arduinoManager.identify()
  container.set('arduinoManager', arduinoManager)

  switches = Switches(container)
  switches.start()
  container.set('switches', switches)

  driver = PWMDriver()
  container.set('PWMDriver', driver)

  platform = MotorizedPlatform(container)
  container.set('platform', platform)

  nav = Navigation(container)
  container.set('navigation', nav)
  
  container.set('scripts', Scripts(container))

  # lidar = Lidar(container)
  # lidar.start()
  # container.set('lidar', lidar)
  ws.start()
  
  def onPos(x, y, t):
    ws.sendData('mainPosition', [x, y, t])

  positionWatcher.setPositionChangedHandler(onPos)

  def app():
    sleep(1)
    platform.stop()
    sleep(1)
    print('> App: READY, all intefaces intialized')
    positionWatcher.reset()
    positionWatcher.start()
    # sleep(1)
    # nav.goTo({'x':600, 'y':600, 'orientation':pi })
    # input('You confirm?')
    # nav.goTo({ 'x': 979, 'y': 1500, 'orientation': pi, 'speed': 40 })
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

