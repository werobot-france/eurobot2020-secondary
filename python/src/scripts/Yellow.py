from math import *
from time import sleep
from ..API import API



"""
angle  = angle-pi
left = right
"""


class Yellow(API):
  
  def run(self):
    self.positionWatcher.reset()
    self.positionWatcher.setIgnoreXChanges(False)
    self.elevator.open()
    self.elevator.reset()
    self.elevator.lighthouse()
    self.elevator.goTo(500)


    self.positionWatcher.setPos(125, 159, 0)

    
    ## DEPLOY LIGHTHOUSE
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=85)
    # click with left
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='right', speed=60)
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=60)
    self.positionWatcher.setPos(125, 159, 0)
    
    self.elevator.goTo(239)
    sleep(0.5)
    self.elevator.goTo(500)
    sleep(0.5)
    ## END OF LIGHTHOUSE DEPLOYMENT
    
    # PRENDRE LES GOBELETS VERTS
    self.positionWatcher.setIgnoreXChanges(True)
    self.navigation.goTo(x=125, y=778, theta=0, speed=60)
    self.positionWatcher.setIgnoreXChanges(False)
    self.navigation.goTo(x=-500, y=778, theta=0, stopOn='front', speed=85)
    
    # ROUTINE POUR PRENDRE
    self.elevator.open()
    self.elevator.goTo(100)
    input('>> continue?')
    self.elevator.close()
    sleep(1)
    self.elevator.goTo(860)
    
    # ALLER POUR TRIER
    self.positionWatcher.setIgnoreXChanges(True)
    self.navigation.goTo(x=0, y=-500, theta=0, stopOn='right', speed=60)
    self.positionWatcher.setIgnoreXChanges(False)
    self.navigation.goTo(x=-500, y=159, theta=0, stopOn='front', speed=85)
    self.navigation.goTo(x=0, y=-500, theta=0, stopOn='right', speed=60)
    self.positionWatcher.setPos(125, 159, 0)
    
    self.positionWatcher.setIgnoreYChanges(True)
    self.navigation.goTo(x=700, y=159, theta=0, speed=60)
    self.positionWatcher.setIgnoreYChanges(False)
    
    self.elevator.goTo(150)
    self.elevator.open()
    sleep(1)
    self.elevator.goTo(600)
    
    self.navigation.goTo(x=800, y=250, theta=pi, speed=60)
    self.navigation.orientTo(theta=pi/2, speed=50)
    
    self.navigation.goTo(x=2500, y=250, theta=pi/2, speed=60)
    
    self.navigation.goTo(x=2500, y=250, theta=pi/2, stopOn='right', speed=60)
    self.navigation.goTo(x=2500, y=-500, theta=pi/2, speed=60)
    