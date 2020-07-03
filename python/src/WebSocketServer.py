from websocket_server import WebsocketServer
import logging
import base64
import json
import re

class WebSocketServer:
  
  def __init__(self, listeningPort = 8082, listeningHost = '0.0.0.0'):
    self.server = WebsocketServer(listeningPort, host=listeningHost)
    self.server.set_fn_new_client(self.onClient)
    self.server.set_fn_message_received(self.onMessage)
  
  def onClient(self, client, server):
    print("> WebSocket: Got a new client", client)
  
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
    if command == 'ping':
      self.send(client, 'pong', 'pong')
    elif command == 'wowo':
      self.send(client, 'pong', 'pong')
    else:
      self.send(client, 'error', 'unknown')

  def send(self, client, responseType, data = None):
    if not client['handler'].keep_alive:
      return False
    toSend = json.dumps({'responseType': responseType, 'data': data})
    # if responseType != 'frame':
    #     print(toSend)
    self.server.send_message(client, toSend)
    return True

  def start(self):
    self.server.run_forever()
