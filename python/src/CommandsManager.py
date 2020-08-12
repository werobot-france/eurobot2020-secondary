import copy

class CommandsManager:
  def __init__(self, container):
    self.container = container
    self.commands = [
      {
        'name': 'ping',
        'description': 'Answer with pong!',
        'arguments': [],
        'handler': self.ping
      },
      {
        'name': 'compo',
        'description': 'Debug command parsing',
        'arguments': -1,
        'handler': self.compo
      },
      {
        'name': 'listCommands',
        'description': 'List all commands',
        'arguments': [],
        'handler': self.listCommands
      },
      {
        'name': 'help',
        'description': 'Help',
        'arguments': [['name', False]],
        'handler': self.help
      },
      {
        'name': 'reset',
        'description': "Will reset the position watcher",
        'arguments': [],
        'handler': self.goTo
      },
      {
        'name': 'goto',
        'description': "It's your slave!",
        'arguments': [['x', True], ['y', True], ['speed', False], ['theta', False], ['stopOn', False]],
        'handler': self.goTo
      },
      {
        'name': 'listScripts',
        'description': 'List files in the script directory',
        'arguments': [],
        'handler': self.listScripts
      },
      {
        'name': 'execScript',
        'description': 'Execute a script, wOw!',
        'arguments': [['name', True]],
        'handler': self.execScript
      },
      {
        'name': 'elevator',
        'description': 'Stepper goto or origin',
        'arguments': [['step', True]],
        'handler': self.elevator
      },
      {
        'name': 'claws',
        'description': 'Set angle of claws servo',
        'arguments': [['angle', True]],
        'handler': self.claws
      },
      {
        'name': 'stop',
        'description': 'Will stop the current running script',
        'arguments': [],
        'handler': self.stop
      }
    ]
    def filter(item):
      item.pop('handler', None)
      return item
    self.newCommands = list(map(filter, copy.deepcopy(self.commands)))
    
  def init(self):
    # self.positionWatcher = self.container.get('positionWatcher')
    # self.navigation = self.container.get('navigation')
    # self.platform = self.container.get('platform')
    self.scripts = self.container.get('scripts')
    #self.elevator = self.container.get('elevator')
  
  '''
  parse the command and return a string with a format type (text or json)
  '''
  def exec(self, rawCommand):
    components = rawCommand.split(' ')
    components = list(filter(lambda c: len(c) > 0, components))
    if len(components) == 0:
      return ''
    commands = list(filter(lambda c: c['name'] == components[0], self.commands))
    if len(commands) == 0:
      return 'Invalid Command!'
    command = commands[0]
    components = components[1:]
    arguments = {}
    if command['arguments'] != -1:
      requiredArguments = 0
      totalArguments = len(command['arguments'])
      
      for arg in command['arguments']:
        if len(arg) > 1 and arg[1]:
          requiredArguments += 1

      if len(components) < requiredArguments:
        return 'Not enought arguments!'
      if len(components) > totalArguments:
        return 'Too much arguments!'

      i = 0
      for arg in components:
        res = arg.split('=')
        index = 0
        key = ''
        value = ''
        if len(res) == 2:
          key = res[0]
          value = res[1]
        else:
          key = command['arguments'][i][0]
          value = res[0]
        
        try:
          value = float(value)
        except ValueError:
          pass
        else:
          if value.is_integer():
            value = int(value)
        
        arguments[key] = value
        i += 1

      #print(arguments)

    return command['handler'](arguments)
  
  def getCommands(self):
    return self.newCommands

  '''''''''
  Commands handlers
  '''''''''
  
  def help(self, components):
    if 'name' in components:
      selectedCommand = None
      for command in self.newCommands:
        if command['name'] == components['name']:
          selectedCommand = copy.deepcopy(command)
      if selectedCommand == None:
        return "Unkown command, invalid command name!"
      selectedCommand['usage'] = selectedCommand['name']
      for arg in selectedCommand['arguments']:
        if len(arg) > 1 and not arg[1]:
          usage = '[' + arg[0] + ']'
        else:
          usage = '{' + arg[0] + '}'
        selectedCommand['usage'] += ' ' + usage
        
      selectedCommand.pop('arguments', None)
      return selectedCommand

    outputStr = {}
    for command in self.newCommands:
      outputStr[command['name']] = command['description']
    return outputStr

  def ping(self, _):
    return "Pong!"
  
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
    print(components)
    #self.navigation.goTo(**components)
  
  def example(self, components):
    return 'OK'
  
  def listCommands(self, components):
    return self.newCommands