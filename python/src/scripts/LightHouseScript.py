from math import *
from time import sleep
from ..API import API

class LightHouseScript(API):
  
  def run(self):
    self.positionWatcher.reset()
    self.positionWatcher.setIgnoreXChanges(False)
    self.elevator.open()
    self.elevator.reset()
    self.elevator.goTo(180, 600)
    self.elevator.sleep()
    
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=75)
    
    # click with left
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=60)
    
    self.positionWatcher.setPos(125, 159, pi)
    
    self.elevator.goTo(40)
    sleep(0.2)
    self.elevator.goTo(400)