import sys
from gpiozero import DigitalInputDevice
from threading import Thread
from time import sleep
from math import *

class PositionWatcher:
  perimeter = 60*pi
  theta = pi
  #theta = (0, 0)
  
  # coté bleu x: 979, y: 159
  x = 979
  y = 159
  
  # left
  phaseA = DigitalInputDevice(6, True)
  phaseB = DigitalInputDevice(16, True)
  
  # right
  phaseC = DigitalInputDevice(20, True)
  phaseD = DigitalInputDevice(21, True)
  
  leftTicks = 0
  rightTicks = 0
  
  leftState = (0, 0)
  leftOldState = (0, 0)
  
  rightState = (0, 0)
  rightOldState = (0, 0)
  
  watchPositionThread = None
  watchTicksThread = None
  enabled = True
  
  oldTicks = (0, 0)
  
  onPositionChangedHandler = None
  
  isTurning = False
  
  L = 120
  l = 161
  
  def watchTicks(self):
    while self.enabled:
      leftFetchedState = (self.phaseA.value, self.phaseB.value)
      rightFetchedState = (self.phaseC.value, self.phaseD.value)
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
        

  def watchPosition(self):
    while self.enabled:
      # LEFT = SIDE
      # RIGHT = BACK
      newTicks = (self.leftTicks, self.rightTicks)
      if (newTicks != self.oldTicks):
          deltaTicks = (newTicks[0] - self.oldTicks[0],
                        newTicks[1] - self.oldTicks[1])
          self.oldTicks = newTicks
          leftDistance = deltaTicks[0] / 2400 * self.perimeter
          rightDistance = deltaTicks[1] / 2400 * self.perimeter
          # t1 = (leftDistance + rightDistance) / 2
          # alpha = (rightDistance - leftDistance) / self.axialDistance
          
          self.x += sin(self.theta)*-rightDistance + cos(self.theta)*leftDistance
          self.y += cos(self.theta)*rightDistance + sin(self.theta)*leftDistance
          
          if self.onPositionChangedHandler != None:
              self.onPositionChangedHandler(self.x, self.y, self.theta)
      sleep(0.01)


  # def watchOrientation(self):
  #   sensor = Driver()
  #   sensor.autoCalibrateGyroOffset()
  #   print("Gyro - Calibration done!")
  #   timeInterval = 0.05
  #   self.theta = pi/2
  #   while (self.enabled):
  #     sleep(timeInterval)
  #     self.theta += radians(((sensor.getRotationZ()[0] * 250.0) / 32768.0) * timeInterval)


  def start(self):
    self.enabled = True
    self.watchTicksThread = Thread(target=self.watchTicks)
    self.watchTicksThread.start()
    self.watchPositionThread = Thread(target=self.watchPosition)
    self.watchPositionThread.start()
    # self.watchOrientationThread = Thread(target=self.watchOrientation)
    # self.watchOrientationThread.start()
    
  def stop(self):
    self.enabled = False

  def getPos(self):
    return (self.x, self.y)

  def getPosRot(self):
    return (self.x, self.y, self.theta * 180/pi)

  def changeIsTurning(self, p):
    self.isTurning = p
    return self.isTurning

  def getOrientation(self):
    return (self.theta)

  def getOrientationDeg(self):
    return (self.theta * 180/pi)
    
  def setOnPositionChangedHandler(self, handler):
    self.onPositionChangedHandler = handler

  def getTicks(self):
    return [self.leftTicks, self.rightTicks]
  
  def targetModeOnChange(self, x, y, theta):
    if self.finished:
      return
    #print(self.targetX, self.targetY, self.threadhold)
    print(x, y)
    dist = hypot(self.targetX-x, self.targetY-y)
    # print(dist)
    if dist <= self.threadhold:
      print('done')
      self.finished = True
  
  def targetMode(self, targetX, targetY, threadhold):
    self.finished = False
    self.targetX = targetX
    self.targetY = targetY
    self.threadhold = threadhold
    self.setOnPositionChangedHandler(self.targetModeOnChange)
    self.start()

## fin de la classe

instance = PositionWatcher()

targetMode = False
continiusMode = False

def onChange(x, y, theta):
  print(str(x) + ";" + str(y) + ";" + str(degrees(theta)))

for arg in sys.argv:
  if arg == '-T':
    targetMode = True
  elif arg == '-C':
    continiusMode = True

if continiusMode:
  instance.setOnPositionChangedHandler(onChange)
  instance.start()

if targetMode:
  cmd = input("").split(';')
  targetX = float(cmd[0])
  targetY = float(cmd[1])
  th = float(cmd[2])
  instance.targetMode(targetX, targetY, th)
  print('ack')
