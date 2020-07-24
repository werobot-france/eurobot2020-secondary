import sys
from src.Container import Container
from src.ArduinoManager import ArduinoManager
from src.Switches import Switches

container = Container()
a = ArduinoManager(container)
a.identify()

s = Switches(container)
def app():
  s.start()
  s.onGroup('front', lambda s: print(s))
  while True:
    pass

try:
  app()
except KeyboardInterrupt:
  print("KeyboardInterrupt")
  s.stop()
  sys.exit()
