import copy

class CommandsManager:
  def __init__(self, container):
    self.container = container
    self.commands = [
      {
        'name': 'ping',
        'description': 'Answer with pong!',
        'arguments': 0,
        'handler': self.ping
      },
      {
        'name': 'compo',
        'description': 'Debug command parsing',
        'arguments': -1,
        'handler': self.compo
      },
      {
        'name': 'goto',
        'description': "It's your slave!",
        'arguments': 2,
        'handler': self.goTo
      },
      {
        'name': 'list_scripts',
        'description': 'List files in the script directory',
        'arguments': 0,
        'handler': self.listScripts
      },
      {
        'name': 'exec_script',
        'description': 'Execute a script, wOw!',
        'arguments': 1,
        'handler': self.execScript
      },
      {
        'name': 'elevator',
        'description': 'Stepper goto or origin',
        'arguments': 1,
        'handler': self.elevator
      },
      {
        'name': 'claws',
        'description': 'Set angle of claws servo',
        'arguments': 1,
        'handler': self.claws
      },
      {
        'name': 'stop',
        'description': 'Will stop the current running script',
        'arguments': 0,
        'handler': self.stop
      }
    ]
    def filter(item):
      item.pop('handler', None)
      return item
    self.newCommands = list(map(filter, copy.deepcopy(self.commands)))
    
  def init(self):
    self.positionWatcher = self.container.get('positionWatcher')
    self.navigation = self.container.get('navigation')
    self.platform = self.container.get('platform')
    self.scripts = self.container.get('scripts')
    self.elevator = self.container.get('elevator')
  
  '''
  parse the command and return a string with a format type (text or json)
  '''
  def exec(self, rawCommand):
    components = rawCommand.split(' ')
    if len(components) == 0:
      return ''
    commands = list(filter(lambda c: c['name'] == components[0], self.commands))
    if len(commands) == 0:
      return 'Invalid Command!'
    command = commands[0]
    if command['arguments'] > 0 and len(components) < (command['arguments'] + 1):
      return 'Not enought arguments!'
    return command['handler'](components[1:])
  
  def getCommands(self):
    return self.newCommands

  '''''''''
  Commands handlers
  '''''''''

  def ping(self, _):
    return 'Pong!'
  
  def compo(self, components):
    return components
  
  def listScripts(self, _):
    return self.scripts.list()
  
  def execScript(self, components):
    return self.scripts.run(components[0])

  def elevator(self, components):
    if len(components) == 1:
      components.append(300)
    components[1] = int(components[1])
    if components[0] == 'origin':
      self.elevator.reset(components[1])
    else:
      components[0] = int(components[0])
      self.elevator.goTo(components[0], components[1])
    return 'OK'

  def claws(self, components):
    if components[0] == 'open':
      self.elevator.open()
    elif components[0] == 'close':
      self.elevator.close()
    else: 
      self.elevator.setClawsAngle(int(components[0]))
    return 'OK'

  def stop(self, _):
    # will stop every thread in the world
    self.navigation.stop()
    self.platform.stop()
    self.scripts.stop()
    self.elevator.stop()
  
  def goTo(self, components):
    targetX = float(components[0])
    targetY = float(components[1])
    theta = float(components[2])
    self.navigation.goTo(targetX, targetY, theta, speed)
  