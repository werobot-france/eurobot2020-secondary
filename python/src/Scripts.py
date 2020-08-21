
import os
import sys
from .ThreadHelper import Thread

class Scripts:
  def __init__(self, container):
    self.container = container
    self.logger = container.get('logger').get('Scripts')
    self.scriptThread = None
    # module = list(map(__import__, ['src.scripts.test_script']))[0].__dict__['scripts'].__dict__['test_script'].__dict__['TestScript']()
    # print(module)
    # sys.exit()

  def run(self, name):
    if (name + '.py') not in os.listdir('src/scripts'):
      return "Invalid script name"
    module = list(map(__import__, ['src.scripts.' + name]))[0].__dict__['scripts'].__dict__[name].__dict__[name]
    script = module(self.container)
    self.logger.info('Starting', name, 'script')
    self.scriptThread = Thread(target=script.run)
    self.scriptThread.start()

  def list(self):
    return os.listdir('src/scripts')

  def stop(self):
    if self.scriptThread != None:
      self.logger.info('A script was stopped')
      self.scriptThread.stop()