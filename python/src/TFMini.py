import serial
import time

class TFMini:
  
  def __init__(self):
    self.serial = serial.Serial("/dev/ttyAMA0", 115200)
  
  def watchDistances(self):
    while True:
      #time.sleep(0.1)
      count = self.serial.in_waiting
      if count > 8:
        recv = self.serial.read(9)
        self.serial.reset_input_buffer()
        if recv[0] == 0x59 and recv[1] == 0x59:
            distance = recv[2] + recv[3] * 256
            strength = recv[4] + recv[5] * 256
            #print('(', distance, ',', strength, ')')
            self.distance = distance * 10
            print(self.distance)
            self.serial.reset_input_buffer()
