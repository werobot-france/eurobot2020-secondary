import serial
from time import sleep
from threading import Thread

class Arduino:
    
    def __init__(self):
        self.serial = serial.Serial(
            port="/dev/ttyUSB0",
            baudrate = 115200, 
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None
        )
        
    def watchPort(self):
        while True:
            line = self.serial.read(1)
            line = line.decode('utf-8')
            print(line)
            
    def startReadThread(self):
        self.readThread = Thread(target=self.watchPort)
        self.readThread.start()

    def init(self):
        print('> Waiting for arduino serial connexion...')
        line = self.serial.readline()
        line = line.decode('utf-8')
        print(line)
        if line.split(':')[0] == "SETUP":
            print("> Serial connexion opened")
            return True
        return False
   
    def sendCommand(self, **options):
        paramsString = ''
        for param in options['params']:
            if isinstance(param, int):
                paramsString += '#' + str(param)
        command = options['name'] + paramsString
        print('command sent:', command)
        self.serial.write(str.encode(command))
        if 'expectResponse' in options and options['expectResponse']:
            # print(self.serial.is_open)
            # self.serial.read(self.serial.in_waiting)
            # print(self.serial.in_waiting)
            line = self.serial.readline()
            print('response expected:', line.decode('utf-8'))
            
