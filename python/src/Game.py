from time import sleep

class Game:
  
  def __init__(self, container):
    self.container = container
    self.server = container.get('websocket')
    self.score = 42

  def arm(self, config):
    print('> Game: Robot armed!')
    print('config', config)
    # wait for the switch to activate
    sleep(3)
    self.onStart()
  
  def onStart(self):
    print('> Game: started!')
    self.server.sendData('gameStart', [])
    # start a 100s timer
    sleep(10)
    self.onEnd()
  
  def onEnd(self):
    print('> Game: end!')
    self.server.sendData('gameEnd', [ self.score ])

  def abort(self):
    print('> Game: aborted!')

