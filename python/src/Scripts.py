
import os

class Scripts:
  def __init__(self, container):
    self.container = container
  
  def run(self, name):
    module = list(map(__import__, ['scripts']))[0].__dict__[name]
    print(module)
    script = module(self.container)
    script.run()
  
  def list(self):
    return os.listdir('src/scripts')