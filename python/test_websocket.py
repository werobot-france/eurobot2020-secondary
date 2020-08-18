from src.WebSocketServer import WebSocketServer
from src.CommandsManager import CommandsManager
from src.Scripts import Scripts
from src.Game import Game
from src.Container import Container
from src.Logger import LoggerManager
from time import sleep

container = Container()

logger = LoggerManager()
logger.setLevel('debug')
container.set('logger', logger)

scripts = Scripts(container)
container.set('scripts', scripts)
  
game = Game(container)
container.set('game', game)

commandsManager = CommandsManager(container)
container.set('commandsManager', commandsManager)

commandsManager.init()

websocket = WebSocketServer(container)
container.set('websocket', websocket)

try:
  logger.startClock()
  websocket.start()
  while True:
    sleep(10)
except KeyboardInterrupt:
  print('')
  websocket.stop()