from time import sleep

class Game:
  
  def __init__(self, container):
    self.container = container
    self.server = container.get('websocket')
    self.score = 42
    
    # blue or yellow
    self.team = 'blue'
    
    # possible values 1, 2 or 3
    self.buosDisposition = 1

  def arm(self, config):
    self.team = config['team']
    self.buosDisposition = config['buosDisposition']
    
    print('> Game: Robot armed! Team: ' + self.team + '; buosDisposition: ' + self.buosDisposition)
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

