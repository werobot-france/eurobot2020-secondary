import serial
import threading

arduino = serial.Serial( port="/dev/ttyUSB0", baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)


def readThread():
    while True:
        line = arduino.readline()
        print(line.decode('utf-8'))

threading.Thread(target=readThread).start()

while True:
    input()
    arduino.write(b"LED\n")
    
    
    CMD#first1#second2#third3#fourth4
    
    
    