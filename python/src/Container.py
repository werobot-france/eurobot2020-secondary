class Container:
  instances = {}
  
  def set(self, name, instance):
    self.instances[name] = instance
  
  def get(self, name):
    if name not in self.instances:
      return None
    return self.instances[name]

  def count(self):
    return len(self.instances)

  def getInstances(self):
    return self.instances
