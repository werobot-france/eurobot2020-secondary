import time
import sys
import os

class TerminalColors:
  HEADER = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  GRAY = '\033[90m'
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
    

class LoggerManager:
  
  levels = {
    'info' : ['INFO', TerminalColors.BLUE],
    'warn' : ['WARN', TerminalColors.YELLOW],
    'error': ['ERRO', TerminalColors.RED],
    'debug': ['DEBU', TerminalColors.GREEN]
  }
  
  def __init__(self):
    self.resetClock()
 
  def resetClock(self):
    self.startedAt = time.time()

  def get(self, name = 'root'):
    return Logger(self, name)
  
  def log(self, message, level = 'info', name = 'root'):
    if level not in self.levels:
      return
    
    level = self.levels[level]
    
    elapsed = time.time() - self.startedAt
    
    line = TerminalColors.GRAY + str(round(elapsed, 3)) + ' - ' +TerminalColors.ENDC 
    line += level[1] + level[0] + TerminalColors.ENDC + TerminalColors.GRAY + ' - ' + TerminalColors.ENDC 
    line += name + ' > '
    line += message
    
    print(line)
  
  
