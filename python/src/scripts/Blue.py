from math import *
from time import sleep
from ..API import API

class Blue(API):

  #start theta 90°

  self.positionWatcher.setPos(2000-175, 122, pi/2)

  
  def run(self):
    """
    yes yes ?
    self.elevator.open(['mid', 'right'])
    self.elevator.reset()
    self.elevator.goTo(500, 600)
    self.elevator.open()
    """
    
    self.positionWatcher.setPos(1100-175, 130, pi/2) # Lrobot/2 = 175 ; lrobot/2 = 122

    # click with right and back
    self.navigation.goTo(x=2000, y=130, theta=pi/2, stopOn='right', speed=70)
    self.navigation.goTo(x=2000, y=-500, theta=pi/2, stopOn='back', speed=60)
    
    self.positionWatcher.setIgnoreXChanges(True)
    self.positionWatcher.setPos(2000-175, 122, pi/2)
    
    # schlag the manches à air
    self.navigation.goTo(x=2000-175, y=700, theta=pi/2, speed=60)

    # click with back and right
    self.navigation.goTo(x=2000, y=-500, theta=pi/2, stopOn='back', speed=60)
    self.navigation.goTo(x=2000, y=122, theta=pi/2, stopOn='right', speed=70)

    self.positionWatcher.setIgnoreXChanges(False)
    self.positionWatcher.setPos(2000-175, 122, pi/2)


    # go south and click back
    self.navigation.goTo(x=1300, y=130, theta=pi/2, speed=60)
    self.navigation.goTo(x=2000, y=-500, theta=pi/2, stopOn='back', speed=60)
