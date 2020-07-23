import os
from .Arduino import Arduino
from joblib import Parallel, delayed

class ArduinoManager:
  def __init__(self, container):
    self.instances = []
    self.container = container
  
  def identify(self):
    # get the list of all the ttyUSBX devices in /dev
    # for each of them create a instance
    devices = os.popen('ls /dev | grep "ttyUSB"').read().split("\n")[0:-1]

    #results = Parallel(n_jobs=-1)(delayed(self.identifySingle)(d) for d in devices)
    results = []
    for d in devices:
      results.append(self.identifySingle(d))

    for device in results:
      name = device.getId()
      if 'STEPPER' in name:
        self.container.set('arduinoStepper', device)
        print('> ArduinoManager: Found STEPPER')
      if 'SWITCHES' in name:
        self.container.set('arduinoSwitches', device)
        print('> ArduinoManager: Found SWITCHES')
    return results

  def identifySingle(self, device):
    instance = Arduino('/dev/' + device)
    instance.init()
    instance.identify()
    return instance
