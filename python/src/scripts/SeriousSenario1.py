from math import *
from time import sleep
from ..API import API

class SeriousSenario1(API):
  
  def run(self):
    self.positionWatcher.reset()
    self.positionWatcher.setIgnoreXChanges(False)
    self.elevator.open()
    self.elevator.reset()
    self.elevator.goTo(500, 600)
    self.elevator.open()
    
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=75)
    
    # click with left
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=60)
    
    self.positionWatcher.setIgnoreXChanges(True)
    self.positionWatcher.setPos(125, 159, pi)
    
    # go to the eceuils
    self.navigation.goTo(x=125, y=925, theta=pi, speed=60)
    self.positionWatcher.setIgnoreXChanges(False)
    
    # approach
    self.navigation.goTo(x=-500, y=925, theta=pi, stopOn='front', speed=75)
    
    self.positionWatcher.setIgnoreXChanges(True)
    self.positionWatcher.setPos(125)
    
    # take buos
    #self.elevator.goTo(300, 600)
    input('> Keep going ?')
    self.elevator.goTo(150, 600)
    #input('> Keep going ?')
    self.elevator.close()
    sleep(0.5)
    self.elevator.goTo(700, 600)
    input('confirm?')
    #input('> Keep going ?')
    
    self.navigation.goTo(x=700, y=-180, theta=pi, speed=75)
    # go back to home
    # self.positionWatcher.setIgnoreXChanges(True)
    # self.navigation.goTo(x=125, y=-500, theta=pi, stopOn='left', speed=60)
    # self.positionWatcher.setIgnoreXChanges(False)
    
    # # click with front and left
    # self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=60)
    # self.positionWatcher.setPos(125, 159, pi)
    # # self.navigation.goTo(x=125, y=-500, theta=pi, stopOn='left', speed=60)
    # # self.positionWatcher.setPos(None, 159, pi)
    # # self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=70)
    # #self.positionWatcher.setPos(125, 159, pi)
    # #self.navigation.goTo(x=125, y=-500, theta=pi, stopOn='left', speed=60)
    
    # #sleep(0.6)
    # self.positionWatcher.setIgnoreXChanges(False)
    # #input('> Keep going ?')
    
    # # go to green chenals
    # self.navigation.goTo(x=700, y=159, theta=pi, speed=60)
    
    input('> Keep going ?')
    self.elevator.goTo(140, 600)
    self.elevator.open(['left'])
    sleep(0.05)
    self.elevator.goTo(500, 600)
    
    #input('> Keep going ?')
    
    # go to purple chenals
    # self.navigation.goTo(x=1250, y=159, speed=60, theta=pi)
    # self.elevator.goTo(140, 600)
    # self.elevator.open(['mid', 'right'])
    # sleep(0.05)
    # self.elevator.goTo(500, 600)
    
    