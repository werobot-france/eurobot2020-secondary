from time import sleep

class Game:
  
  def __init__(self, container):
    self.container = container
    self.server = container.get('websocket')
    self.logger = self.container.get('logger').get('Game')
    self.score = 42
    
    # blue or yellow
    self.team = 'blue'
    
    # possible values 1, 2 or 3
    self.buosDisposition = 1

  def arm(self, config):
    self.team = config['team']
    self.buosDisposition = config['buosDisposition']
    
    self.logger.info('Robot armed!', config)
    # wait for the switch to activate
    sleep(3)
    self.onStart()
  
  def onStart(self):
    self.logger.info('Started')
    self.server.sendData('gameStart', [])
    # start a 100s timer
    sleep(10)
    self.onEnd()
  
  def onEnd(self):
    self.logger.info('End!')
    self.server.sendData('gameEnd', [ self.score ])

  def abort(self):
    print('> Game: aborted!')

