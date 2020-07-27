from src.Lidar import Lidar
from src.Container import Container
from src.WebSocketServer import WebSocketServer
from src.PositionWatcher import PositionWatcher

container = Container()

pw = PositionWatcher()
pw.start()
container.set('positionWatcher', pw)

ws = WebSocketServer()
ws.start()
container.set('websocket', ws)

l = Lidar(container)
l.start()

print('READY!')
