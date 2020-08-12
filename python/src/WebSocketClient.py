import websocket
import json
from time import sleep
from .ThreadHelper import Thread
import random
import time

class WebSocketClient:

  def __init__(self, identifier = ''):
    self.message = ''
    if identifier == '':
      identifier = 'terminal_' + str(random.randint(1000, 9999)) + '_' + str(round(time.time(), 3))
    self.identifier = identifier
    self.ws = None
    self.mainThread = None
    self.onOpenHandler = None
    self.callback = None

  def run(self):
    websocket.enableTrace(False)
    def onMessage(ws, message = ""): 
      print(message)
      self.onMessage(ws, message)
    def onError(ws, err): self.onError(ws, err)
    def onClose(ws): self.onClose(ws)
    def onOpen(ws): self.onOpen(ws)
    self.ws = websocket.WebSocketApp(
      'ws://localhost:8082/?identifier=' + self.identifier,
      on_message = onMessage,
      on_error = onError,
      on_close = onClose,
      on_open = onOpen
    )
    self.ws.onOpen = self.onOpen
    self.ws.run_forever()
    print('> WebSocketClient: end of the client')
    sleep(1)
    self.run()
  
  def start(self):
    self.mainThread = Thread(target=self.run)
    self.mainThread.start()
  
  def send(self, command, args, callback = None):
    toSend = json.dumps({'command': command, 'args': args})
    #print(toSend)
    self.callback = callback
    print(callback)
    self.ws.send(toSend)
    
  def onOpen(self, ws):
    print('> WebSocketClient: connexion opened')
    if self.onOpenHandler != None:
      self.onOpenHandler()
    
  def onClose(self, ws):
    print('> WebSocketClient: connexion closed')
 
  def onError(self, ws, error):
    print(error)
    
  def onMessage(self, ws, message):
    print(message, self.callback)
    if self.callback != None:
      self.callback(message)
