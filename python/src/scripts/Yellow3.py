from math import *
from time import sleep
from ..API import API

class Yellow3(API):
  
  def run(self):
    # theta = 0
    self.positionWatcher.setPos(None, None, 0)
    
    self.positionWatcher.reset()
    self.schlager.open()
    self.positionWatcher.setIgnoreXChanges(False)
    self.elevator.open()
    self.elevator.reset()
    self.elevator.lighthouse()
    self.elevator.goTo(500)
    self.schlager.close()
    
    ## DEPLOY LIGHTHOUSE
    # click with front
    self.positionWatcher.setIgnoreYChanges(True)
    self.navigation.goTo(x=-500, y=159, theta=0, stopOn='front', speed=85)
    self.positionWatcher.setIgnoreYChanges(False)
    # click with left
    self.navigation.goTo(x=0, y=-500, theta=0, stopOn='right', speed=60)
    # click with front
    self.navigation.goTo(x=-500, y=159, theta=0, stopOn='front', speed=60)
    
    self.positionWatcher.setPos(125, 159, 0)
    
    self.elevator.goTo(239)
    sleep(0.5)
    self.elevator.goTo(500)
    sleep(0.5)
    ## END OF LIGHTHOUSE DEPLOYMENT
    
    # PRENDRE LES GOBELETS VERTS
    self.positionWatcher.setIgnoreXChanges(True)
    self.navigation.goTo(x=125, y=773, theta=0, speed=60)
    self.positionWatcher.setIgnoreXChanges(False)
    self.navigation.goTo(x=-500, y=773, theta=0, stopOn='front', speed=85)
    
    # ROUTINE POUR PRENDRE
    self.elevator.open()
    self.elevator.goTo(100)
    input('>> continue?')
    self.elevator.close()
    sleep(1)
    self.elevator.goTo(860)
    
    # ALLER POUR TRIER en passant par le lighthouse
    self.positionWatcher.setIgnoreXChanges(True)
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    self.positionWatcher.setIgnoreXChanges(False)
    self.navigation.goTo(x=-500, y=159, theta=pi, stopOn='front', speed=85)
    self.navigation.goTo(x=0, y=-500, theta=pi, stopOn='left', speed=60)
    self.positionWatcher.setPos(125, 159, pi)
    
    self.positionWatcher.setIgnoreYChanges(True)
    self.navigation.goTo(x=700, y=159, theta=pi, speed=60)
    self.positionWatcher.setIgnoreYChanges(False)
    
    # Lâcher les gobelets
    self.elevator.goTo(150)
    self.elevator.open()
    sleep(1)
    self.elevator.goTo(600)
    
    # se réorienter pour aller vers les manches à air
    self.navigation.goTo(x=800, y=250, theta=pi, speed=60)
    self.navigation.orientTo(theta=pi/2, speed=50)
    
    self.navigation.goTo(x=1750, y=250, theta=pi/2, speed=60)

    self.navigation.goTo(x=2500, y=250, theta=pi/2, stopOn='right', speed=60)
        
    self.positionWatcher.setPos(1875, 250, pi/2)
    
    # on se recale par rapport au mur de derrière
    self.navigation.goTo(x=1875, y=-600, theta=pi/2, stopOnSlip=True, speed=70)
    
    self.positionWatcher.setPos(1875, 159, pi/2)
    
    self.navigation.goTo(x=2600, y=250, theta=pi/2, stopOn='right', speed=80)
    
    self.positionWatcher.setPos(1875, 159, pi/2)
    
    self.schlager.open()
    
    self.positionWatcher.setIgnoreXChanges(False)
    self.positionWatcher.setIgnoreYChanges(True)
    self.navigation.goTo(x=1875, y=500, theta=pi/2, speed=85)
    
    self.navigation.goTo(x=2600, y=500, theta=pi/2, stopOn='right', speed=80)
    self.positionWatcher.setPos(1875, 450, pi/2)
    
    self.navigation.goTo(x=1875, y=750, theta=pi/2, speed=85)
    self.positionWatcher.setIgnoreYChanges(False)
    # fin du schlagague
    
    #  RETOUR AU SUD ??
    self.navigation.goTo(x=1700, y=750, theta=pi/2, speed=85)
    self.navigation.orientTo(theta=3*pi/2, speed=50)
    
    # on se recalle en y = 0
    self.positionWatcher.setIgnoreYChanges(True)
    self.navigation.goTo(x=1700, y=-500, theta=3*pi/2, stopOn='front', speed=80)
    self.positionWatcher.setIgnoreYChanges(False)
    self.positionWatcher.setPos(1700, 159, 3*pi/2)
    self.navigation.goTo(x=2600, y=-500, theta=3*pi/2, stopOn='left', speed=80)
    self.positionWatcher.setPos(1875, 159, 3*pi/2)
    
    # INSERT GOBLEET??? PRIVE
    
    self.positionWatcher.setIgnoreXChanges(True)
    # retour approximatif dans la zone sud
    self.navigation.goTo(x=700, y=159, theta=3*pi/2, speed=80)
    self.positionWatcher.setIgnoreXChanges(False)
    
    
    
    