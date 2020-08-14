from .ThreadHelper import Thread
from datetime import datetime
import json
import time
import sys
import os

class TerminalColors:
  PURPLE = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  GRAY = '\033[90m'
  CYAN = '\033[96m'
  LIGHT = '\033[38;5;244m'
  BLACK = '\033[30m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  ENDC = '\033[0m'

class Logger:
  def __init__(self, manager, name):
    self.manager = manager
    self.name = name
    
  def log(self, message, level):
    self.manager.log(message, level, self.name)

  def debug(self, message):
    self.log(message, 'debug')
  
  def info(self, message):
    self.log(message, 'info')
  
  def warn(self, message):
    self.log(message, 'warn')
    
  def error(self, message):
    self.log(message, 'error')
    
  def data(self, data):
    return json.dumps(data)

class LoggerManager:
  
  levels = {
    'debug': ['DEBU', TerminalColors.GREEN],
    'info' : ['INFO', TerminalColors.BLUE],
    'warn' : ['WARN', TerminalColors.YELLOW],
    'error': ['ERRO', TerminalColors.RED]
  }
  
  outputLevel = 0
  
  sessionLines = None
  sessionFileName = None
  
  shortTermFile = None
  shortTermPath = '/python-recovery/logs'
  
  longTermPath = './logs'
  
  def __init__(self):
    self.resetClock()
 
  def resetClock(self):
    self.startedAt = time.time()

  def get(self, name = 'root'):
    return Logger(self, name)

  def setLevel(self, level = 'info'):
    self.outputLevel = list(self.levels.keys()).index(level)
  
  def log(self, message, level = 'info', name = 'root'):
    if level not in self.levels:
      return
    
    if list(self.levels.keys()).index(level) < self.outputLevel:
      return
    
    level = self.levels[level]
    
    elapsed = time.time() - self.startedAt
    
    line = TerminalColors.GRAY + str(round(elapsed, 3)) + ' - ' +TerminalColors.ENDC 
    line += level[1] + level[0] + TerminalColors.ENDC + TerminalColors.GRAY + ' - ' + TerminalColors.ENDC 
    line += TerminalColors.LIGHT + name + TerminalColors.GRAY + ' > ' + TerminalColors.ENDC
    line += message
    
    # record the message in a temporary file
    # if self.sessionLines != None:
    #   print('wow')
    #   self.shortTermFile.write(line + "\n")
    #   self.sessionLines.append(line)
    
    print(line)
    
  # def save(self):
  #   if self.sessionFileName == None:
  #     return
  #   longTermFile = open(self.longTermPath + '/' + self.sessionFileName, 'a')
  #   toWrite = '\n'.join(self.sessionLines)
  #   longTermFile.write(toWrite)
  #   self.sessionLines = []
  #   longTermFile.close()
  #   self.shortTermFile.close()
  #   self.shortTermFile = open(self.shortTermPath + '/' + self.sessionFileName, 'a')
  #   print('saved')
  
  # def saveThread(self):
  #   while True:
  #     time.sleep(2)
  #     self.save()
  
  # def startRecording(self, sessionName = 'default'):
  #   now = datetime.now()
  #   self.sessionFileName = now.strftime("%a_%d-%m-%Y_%H-%M-%s") + '__' + sessionName + '.txt'
  #   self.shortTermFile = open(self.shortTermPath + '/' + self.sessionFileName, 'a')
  #   self.sessionLines = []
  #   # every 10 seconds, record in a actual file
  #   self.savingThread = Thread(target=self.saveThread)
  #   self.savingThread.start()
    
  # def stopRecording(self):
  #   self.shortTermFile.close()
  #   self.sessionFileName = None
  #   self.sessionLines = None
  #   self.savingThread = Thread(target=self.saveThread)
  #   self.savingThread.stop()
  #   self.saveThread()
