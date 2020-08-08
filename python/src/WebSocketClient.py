import websocket
import json
from time import sleep

class WebSocketClient:

  def __init__(self):
    self.ws = None

  def start(self):
    websocket.enableTrace(True)
    def onMessage(ws, message = ""): self.onMessage(ws, message)
    def onError(ws, err): self.onError(ws, err)
    def onClose(ws): self.onClose(ws)
    def onOpen(ws): self.onOpen(ws)
    self.ws = websocket.WebSocketApp(
      "ws://localhost:8082/?identifier=secondary",
      on_message = onMessage,
      on_error = onError,
      on_close = onClose,
      on_open = onOpen
    )
    self.ws.onOpen = self.onOpen
    self.ws.run_forever()
    print('> WebSocketClient: end of the client')
    sleep(1)
    self.start()
  
  def send(self, command, args):
    toSend = json.dumps({'command': command, 'args': args})
    print(toSend)
    self.ws.send(toSend)
    
  def onOpen(self, ws):
    print('> WebSocketClient: connexion opened')
    
  def onClose(self, ws):
    print('> WebSocketClient: connexion closed')
 
  def onError(self, ws, error):
    print(error)
    
  def onMessage(self, ws, message):
    print(message)
