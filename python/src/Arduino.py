import serial
import time
from .ThreadHelper import Thread

class Arduino:
  name = ''

  def __init__(self, path, baudrate = 9600):
    self.logger = self.container.get('logger').get('Arduino')
    self.serial = serial.Serial(
      port = path,
      baudrate = baudrate,
      parity = serial.PARITY_NONE,
      stopbits = serial.STOPBITS_ONE,
      bytesize = serial.EIGHTBITS,
      timeout = 2
    )
    
  def getName(self):
    return self.name

  # def watchPort(self):
  #   while True:
  #     line = self.serial.read(1)
  #     line = line.decode('utf-8')
  #     print(line)

  # def startReadThread(self):
  #   self.readThread = Thread(target=self.watchPort)
  #   self.readThread.start()

  def readLine(self):
    l = self.serial.readline()
    return l.decode('utf-8')

  def init(self):
    self.logger.info("Waiting for arduino serial connexion...")
    line = ''
    while "Pong!" not in line:
      line = self.sendCommand(
        name = "PING",
        expectResponse = True,
        noFilter = True
      )
    self.logger.info("Initialized!")
    
  def identify(self):
    line = self.sendCommand(
      name = "ID",
      expectResponse = True
    )
    self.name = line.split("ID:")[1][0:-1]
    return self.name
  
  def setName(self, name):
    self.name = name

  def sendCommand(self, **options):
    paramsString = ''
    if 'params' in options:
      for param in options['params']:
        if isinstance(param, int):
          paramsString += '#' + str(param)
        else: 
          paramsString += '#' + param
    command = options['name'] + paramsString
    #print('command sent:', command , 'on device', self.name)

    name = self.name
    if len(name) > 0:
      name = name + ':'

    self.logger.debug(name + ' --> ' + command)
    self.serial.write(str.encode(command))
    if 'expectResponse' in options and options['expectResponse']:
      # print(self.serial.is_open)
      # self.serial.read(self.serial.in_waiting)
      # print(self.serial.in_waiting)
      if 'noFilter' in options and options['noFilter']:
        line = self.readLine()
      else:
        line = ''
        while len(line) < 2:
          line = self.readLine()
          #print(line)
      #print('response expected:', line)
      
      self.logger.debug(name + ' <-- ' + line.replace('\n', ''))
      return line
        
