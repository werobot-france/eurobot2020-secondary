from websocket_server import WebsocketServer
import logging
import base64
import json
import re
from threading import Thread

class WebSocketServer:
  clients = []
  mainThread = None

  def __init__(self, container, listeningPort = 8082, listeningHost = '0.0.0.0'):
    #self.navigation = container.get('navigation')
    self.container = container
    self.server = WebsocketServer(listeningPort, host=listeningHost)
    self.server.set_fn_new_client(self.onClient)
    self.server.set_fn_message_received(self.onMessage)
    self.server.set_fn_client_left(self.onDisconnect)
    self.game = None

  def onClient(self, client, _):
    print("> WebSocket: Got a new client", client)
    print(client['address'])
    self.clients.append(client)

  def onDisconnect(self, client, _):
    print("> WebSocket: Client left", client)
    self.clients = []

  def onMessage(self, client, server, message):
    print("> Got a new message", message)
    # We parse the json of the message
    messageParsed = json.loads(message)

    # just a sanity check to check for useless things to check olalalal
    if not ('command' in messageParsed and 'args' in messageParsed):
      print("> WARN: Olalalalla j'ai vu un message qui n'est pas très très attendu qu'est ce que c'est que ce bordel je me demande vraiment olalal")
      return

    command = messageParsed['command']
    args = messageParsed['args']
    print(command, args)
    if command == 'ping':
      self.send(client, 'pong', 'pong')
    elif command == 'wowo':
      self.send(client, 'pong', 'pong')
    elif command == 'arm':
      self.game.arm(args)
    elif command == 'abort':
      self.game.abort()
    elif command == 'goTo':
      args['x'] = float(args['x'])
      args['y'] = float(args['y'])
      args['speed'] = float(args['speed'])
      #self.navigation.goTo(args)
    else:
      self.send(client, 'error', 'unknown')

  def send(self, client, responseType, data = None):
    if not client['handler'].keep_alive:
      return False
    toSend = json.dumps({'responseType': responseType, 'data': data})
    # if responseType != 'frame':
    #     print(toSend)
    #print(toSend)
    self.server.send_message(client, toSend)
    return True

  def sendData(self, type, data):
    if len(self.clients) == 0:
      return False

    return self.send(self.clients[0], type, data)

  def start(self):
    self.game = self.container.get('game')
    self.mainThread = Thread(target=self.server.run_forever)
    self.mainThread.start()

  def stop(self):
    self.server.server_close()