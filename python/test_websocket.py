from src.WebSocketServer import WebSocketServer

from src.Game import Game
from src.Container import Container

container = Container()

server = WebSocketServer(container)
container.set('websocket', server)

game = Game(container)
container.set('game', game)

server.start()

print('ready \n')

# while True:
#   toSend = input('>')
#   if toSend == 'start':
#     server.sendData('matchStart', [])
#   if toSend == 'end':
#     server.sendData('matchEnd', [])