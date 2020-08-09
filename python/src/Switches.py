from .ThreadHelper import Thread

class Switches:
  
  watchStateThread = None
  watchStateEnabled = False
  
  left = False
  right = False
  front = False
  
  groups = { 'L': 'left', 'R': 'right', 'F': 'front' }
  
  handlers = { 'leftHandler': None, 'rightHandler': None, 'frontHandler': None }
  
  state = { 'right': False, 'left': False, 'front': False }
  
  def __init__(self, container):
    self.arduino = container.get('arduinoSwitches')
    
  def onGroup(self, name, handler):
    if name + 'Handler' not in self.handlers:
      print('WARN: Not valid group name')
      return
    self.handlers[name + 'Handler'] = handler
    
  def watchState(self):
    while self.watchStateEnabled:
      line = ''
      while len(line) < 2 and self.watchStateEnabled:
        line = self.arduino.readLine()
        if len(line) == 0:
          break
        comp = line[0:4].split(':')
        #print(comp[0])
        if comp[0] not in self.groups:
          break
        name = self.groups[comp[0]]
        state = comp[1] == 'ON'
        print(name + '=' + str(state))
        handler = self.handlers[name + 'Handler']
        if handler != None:
          handler(state)
        self.state[name] = state
        print(self.state)
        # if comp[0] == 'L':
        #   self.left = state
        # elif comp[0] == 'R':
        #   self.right = state
        # elif comp[0] == 'F':
        #   self.front = state

  def start(self):
    if self.watchStateThread == None:
      print('> Switches: Started watch thread')
      self.watchStateEnabled = True
      self.watchStateThread = Thread(target=self.watchState)
      self.watchStateThread.start()
      
  def stop(self):
    self.watchStateEnabled = False
    self.watchStateThread.stop()
    
  def getState(self, name):
    if name not in self.state:
      return False
    return self.state[name]