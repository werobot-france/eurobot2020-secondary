from math import *
from time import sleep
from ..API import API

class WithSwitch(API):

  def run(self):
    
    self.positionWatcher.setPos(1100-175, 130, 3*pi/2) # Lrobot/2 = 175 ; lrobot/2 = 122

    # click with riht and front
    self.navigation.goTo(x=2000, y=130, theta=3*pi/2, stopOn='right', speed=70)
    self.navigation.goTo(x=2000, y=-500, theta=3*pi/2, stopOn='front', speed=60)
    
    self.positionWatcher.setIgnoreXChanges(True)
    self.positionWatcher.setPos(2000-175, 122, 3*pi/2)
    
    # schlag the manches à air
    self.navigation.goTo(x=2000-175, y=700, theta=3*pi/2, speed=60)

    # click with front and right
    self.navigation.goTo(x=2000, y=-500, theta=3*pi/2, stopOn='front', speed=60)
    self.navigation.goTo(x=2000, y=122, theta=3*pi/2, stopOn='right', speed=70)

    self.positionWatcher.setIgnoreXChanges(False)
    self.positionWatcher.setPos(2000-175, 122, 3*pi/2)


    # go south and click front
    self.navigation.goTo(x=1300, y=130, theta=3*pi/2, speed=60)
    self.navigation.goTo(x=2000, y=-500, theta=3*pi/2, stopOn='front', speed=60)
