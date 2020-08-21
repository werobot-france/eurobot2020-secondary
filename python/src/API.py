class API:
  def __init__(self, container):
    self.navigation = container.get('navigation')
    self.positionWatcher = container.get('positionWatcher')
    self.elevator = container.get('elevator')