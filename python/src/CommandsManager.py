import copy

class CommandsManager:
  def __init__(self, container):
    self.container = container
    self.commands = [
      {
        'name': 'ping',
        'description': 'Answer with pong!',
        'handler': self.ping
      },
      {
        'name': 'compo',
        'description': 'Debug command parsing',
        'handler': self.compo
      },
      {
        'name': 'list_scripts',
        'description': 'List files in the script directory',
        'handler': self.listScripts
      }
    ]
    
  def init(self):
    self.positionWatcher = container.get('positionWatcher')
    self.navigation = container.get('navigation')
    self.scripts = container.get('scripts')
  
  '''
  parse the command and return a string with a format type (text or json)
  '''
  def exec(self, rawCommand):
    components = rawCommand.split(' ')
    command = list(filter(lambda c: c['name'] == components[0], self.commands))[0]
    print(command)
    return command['handler'](components[1:])
  
  def getCommands(self):
    def filter(item):
      item.pop('handler', None)
      return item
    return list(map(filter, copy.deepcopy(self.commands)))
  
  
  '''''''''
  Commands handlers
  '''''''''

  def ping(self, _):
    return 'Pong!'
  
  def compo(self, components):
    return components
  
  def listScripts(self, _):
    return self.scripts.list()
  