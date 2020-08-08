from math import *
import time
from time import sleep

'''
This class manage all the movement of the robot motorized platform
'''
class Navigation:
  def __init__(self, container):
    self.platform = container.get('platform')
    self.positionWatcher = container.get('positionWatcher')
    #self.switches = container.get('switches')
    self.enabled = False

  '''
  Private
  '''
  def getSpeedFromAngle(self, targetAngle, speed):
    ta = pi - (targetAngle - self.positionWatcher.theta)
    return [
      cos(ta+3*pi/4) * speed,
      sin(ta+3*pi/4) * speed,
      sin(ta+3*pi/4) * speed,
      cos(ta+3*pi/4) * speed,
    ]

  '''
  @Private
  '''
  def getPlatformSpeed(self, initialDist, dist, maxSpeed, minSpeed):
    p = abs(initialDist - dist)
    if p <= 25:
      return self.saturation(0, 25, minSpeed, maxSpeed, p)
    else:
      l = maxSpeed - minSpeed
      k = 0.04
      o = 100
      return (l/(1+exp(-(k*(dist - o))))) + minSpeed

  '''
  @Private
  '''
  def saturation(self, minX, maxX, minY, maxY, value):
    # minX = 10*10
    # maxX = 100*10
    # minY = 10
    # maxY = 100
    minX *= 10
    maxX *= 10
    if value <= minX:
      print('Very start thing case')
      return minY
    elif value >= maxX:
      print('Normal cruise')
      return maxY
    else:
      print('Start thing case')
      a = (maxY-minY)/(maxX - minX)
      b = minY - a*minX
      return a * value + b

  '''
  Public
  '''
  def goTo(self, options):
    print(options)

    # targetX, targetY, speed=50, threshold=5, orientation=None
    
    targetX = options['x']
    targetY = options['y']
    if 'orientation' in options:
      orientation = options['orientation']
    else:
      orientation = None
      
    if 'threshold' in options:
      threshold = options['threshold']
    else:
      threshold = 5
          
    if 'speed' in options:
      speed = options['speed']
    else:
      speed = 50

    #self.positionWatcher.pauseWatchPosition()
    minSpeed = 25
    if speed < minSpeed:
      speed = minSpeed
    self.done = False
    targetAngle = atan2(targetY, targetX)
    print("> Navigation: going to (x: %(x)f y: %(y)f) with a angle of %(a)f deg" % {
      'x': targetX,
      'y': targetY,
      'a': degrees(targetAngle)
    })
    #self.setSpeed(self.getSpeedFromAngle(targetAngle, speed))
    initialDist = None
    while not self.done:
      #x, y, theta = self.positionWatcher.computePosition()
      x, y, theta = self.positionWatcher.getPos()
      dist = sqrt((targetX - x)**2 + (targetY - y)**2)

      print("\n\nx:", round(x, 0))
      print("y:", round(y, 0))
      print("theta:", round(degrees(theta), 0))

      if initialDist == None:
        initialDist = dist
      if dist <= threshold:
        self.done = True
      else:
        targetAngle = (atan2(targetY - y, targetX - x))%(2*pi)
        print("targetAngle:", round(degrees(targetAngle), 2))
        s = self.getPlatformSpeed(initialDist, dist, speed, minSpeed)
        #print("speed", s)
        b = self.getSpeedFromAngle(targetAngle, s)

        if orientation != None:
          c = (theta - orientation)/2*pi
          if abs(c*speed) <= speed/4:
            cmd = c*speed
          else:
            cmd = speed/4*c/abs(c)
          cmds = [
            cmd,
            cmd,
            -cmd,
            -cmd
          ]
          for i in range(4):
            b[i] += cmds[i]
            
        #print("\nMotors:", b, "\n\n\n\n")
        self.platform.setSpeed(b)
        
        # if 'stopOn' in options:
        #     self.done = self.switches.getState(options.stopOn)

    #self.positionWatcher.resumeWatchPosition()
    self.platform.stop()
    print('End of goTo')

  '''
  Public
  '''
  def relativeGoTo(self, targetDeltaX, targetDeltaY, speed=50, threshold=5, orientation=None):
    self.positionWatcher.pauseWatchPosition()
    x, y, theta = self.positionWatcher.computePosition()
    targetX = x + cos(theta)*targetDeltaX + sin(theta)*targetDeltaY
    targetY = y + sin(theta)*targetDeltaX + cos(theta)*targetDeltaY
    self.goTo(targetX, targetY, speed, threshold, orientation)

  '''
  Public
  '''
  def orientTo(self, orientation, speed=30, threshold=pi/32):
    self.positionWatcher.pauseWatchPosition()
    theta = self.positionWatcher.computePosition()[2]
    while abs(theta - orientation) > threshold:
      theta = self.positionWatcher.computePosition()[2]
      c = (theta - orientation)/abs(theta - orientation)
      speeds = [
        c*speed,
        c*speed,
        -c*speed,
        -c*speed
      ]
      self.platform.setSpeed(speeds)
      print("\n\nc:", c)
      print("deltaOrientation:", theta - orientation)
    
    self.positionWatcher.resumeWatchPosition()
    self.platform.stop()
    print('End of orientTo')

  '''
  Public
  '''
  def goToPath(self, path):
    for node in path:
      self.goTo(node)
      sleep(0.5)

    self.platform.stop()
    print('Path done')
