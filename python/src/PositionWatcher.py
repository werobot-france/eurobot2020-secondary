from gpiozero import DigitalInputDevice
from threading import Thread
import time
from math import *

from BMI160_i2c import Driver

'''
This class manage all the odometry operations
'''
class PositionWatcher:
  backPerimeter = 90*pi
  lateralPerimeter = 60*pi
  #theta = 3*pi/2
  
  theta = pi
  
  # coté bleu x: 979, y: 159
  x = 979
  y = 159

  # left (scotch bleu) encodeur branché sur la prise du milieur
  phaseA = DigitalInputDevice(20, True)
  phaseB = DigitalInputDevice(21, True)
  
  # right (sans scotch) encodeur branché côté carte sd
  phaseC = DigitalInputDevice(16, True)
  phaseD = DigitalInputDevice(6, True)

  # back  (scotch vert) encodeur branché coté port USB
  phaseE = DigitalInputDevice(5, True)
  phaseF = DigitalInputDevice(19, True)
  
  leftTicks = 0
  rightTicks = 0
  backTicks = 0
  
  leftState = (0, 0)
  leftOldState = (0, 0)
  
  rightState = (0, 0)
  rightOldState = (0, 0)
  
  backState = (0, 0)
  backOldState = (0, 0)
  
  watchPositionThread = None
  watchTicksThread = None
  
  oldTicks = (0, 0, 0)

  # distance entre les deux encodeurs latéraux (milieux) (arrête de la base)
  axialDistance = 280
  
  # distance entre l'encodeur arrirère et la droite qui passe par les deux encodeurs latéraux
  backAxialDistance = 110
  
  watchTicksEnabled = False
  watchPositionEnabled = False

  positionChangedHandler = None

  def __init__(self):
    print("Pos watcher init")
  
  '''
  This thread will keep updated the left, right and back tick count
  '''
  def watchTicks(self):
    while self.watchTicksEnabled:
      leftFetchedState = (self.phaseA.value, self.phaseB.value)
      rightFetchedState = (self.phaseC.value, self.phaseD.value)
      backFetchedState = (self.phaseE.value, self.phaseF.value)
      if leftFetchedState != self.leftState:
        self.leftState = leftFetchedState

        if self.leftState[0] == self.leftOldState[1]:
          self.leftTicks -= 1
        else:
          self.leftTicks += 1

        self.leftOldState = self.leftState

      if rightFetchedState != self.rightState:
        self.rightState = rightFetchedState

        if self.rightState[0] == self.rightOldState[1]:
          self.rightTicks -= 1
        else:
          self.rightTicks += 1

        self.rightOldState = self.rightState

      if backFetchedState != self.backState:
        self.backState = backFetchedState

        if self.backState[0] == self.backOldState[1]:
          self.backTicks -= 1
        else:
          self.backTicks += 1

        self.backOldState = self.backState

  '''
  /!\ Call once
  '''
  def computePosition(self):
    newTicks = (self.leftTicks, self.rightTicks, self.backTicks)
    if (newTicks != self.oldTicks):
      deltaTicks = (
        newTicks[0] - self.oldTicks[0],
        newTicks[1] - self.oldTicks[1],
        newTicks[2] - self.oldTicks[2]
      )
      self.oldTicks = newTicks
      
      leftDistance = deltaTicks[0] / 2400 * self.lateralPerimeter
      rightDistance = deltaTicks[1] / 2400 * self.lateralPerimeter
      backDistance = deltaTicks[2] / 2400 * self.backPerimeter

      #deltaTheta = 2 * asin((rightDistance - tb) / self.axialDistance)
      deltaTheta = (rightDistance - leftDistance) / self.axialDistance
      
      tb = (leftDistance + rightDistance) / 2
      backDistance -= deltaTheta*self.backAxialDistance
      
      self.x += cos(self.theta) * tb + sin(self.theta) * backDistance
      self.y += sin(self.theta) * tb - cos(self.theta) * backDistance
      self.theta += deltaTheta
      
      if self.positionChangedHandler != None:
        self.positionChangedHandler(self.x, self.y, self.theta)

    return (self.x, self.y, self.theta)

  def watchPosition(self):
    while self.watchPositionEnabled:
      self.computePosition()
      time.sleep(0.01)

  def startWatchTicks(self):
    if not self.watchTicksEnabled:
      self.watchTicksEnabled = True
      self.watchTicksThread = Thread(target=self.watchTicks)
      self.watchTicksThread.start()
  
  def startWatchPosition(self):
    if not self.watchPositionEnabled:
      self.watchPositionEnabled = True
      self.watchPositionThread = Thread(target=self.watchPosition)
      self.watchPositionThread.start()
      
  def start(self):
    self.startWatchTicks()
    self.startWatchPosition()

  def isEnabled(self):
    return self.enabled

  def stop(self):
    self.watchTicksThread = False
    self.watchPositionThread = False

  def getTicks(self):
    return [self.leftTicks, self.rightTicks, self.backTicks]
  
  def pauseWatchPosition(self):
    self.watchPositionThread = False
    
  def resumeWatchPosition(self):
    self.startWatchPosition()

  def setPositionChangedHandler(self, handler):
    self.positionChangedHandler = handler

  def getData(self):
    return [self.x, self.y, self.theta]