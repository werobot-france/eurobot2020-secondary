import smbus
import time

class CharacterLCD:
    
    i2cBus = 1
    i2cAddress = 0x27
    lcdWidth = 16

    characterMode = 1 # Mode - Sending data
    commandMode = 0 # Mode - Sending command

    firstLine = 0x80 # LCD RAM address for the 1st line
    secondLine = 0xC0 # LCD RAM address for the 2nd line
    thirdLine = 0x94 # LCD RAM address for the 3rd line
    fourthLine = 0xD4 # LCD RAM address for the 4th line
    
    backlightOn = 0x08
    backlightOff = 0x00 
    enable = 0b00000100 # Enable bit
    
    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    
    def __init__(self, **options):
        if 'i2cAddress' in options:
            self.i2cAddress = options['i2cAddress']
        if 'lcdWidth' in options:
            self.lcdWidth = options['lcdWidth']
        if 'i2cBus' in options:
            self.i2cBus = options['i2cBus']
        self.bus = smbus.SMBus(self.i2cBus)
        
    def toggleEnable(self, bits):
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.i2cAddress, (bits | self.enable))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.i2cAddress, (bits & ~self.enable))
        time.sleep(self.E_DELAY)

    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command
    def sendByte(self, bits, mode):
        bitsHigh = mode | (bits & 0xF0) | self.backlightOn
        bitsLow = mode | ((bits<<4) & 0xF0) | self.backlightOn

        # High bits
        self.bus.write_byte(self.i2cAddress, bitsHigh)
        self.toggleEnable(bitsHigh)

        # Low bits
        self.bus.write_byte(self.i2cAddress, bitsLow)
        self.toggleEnable(bitsLow)
    
    def initialise(self):
        self.sendByte(0x33, self.commandMode) # 110011 Initialise
        self.sendByte(0x32, self.commandMode) # 110010 Initialise
        self.sendByte(0x06, self.commandMode) # 000110 Cursor move direction
        self.sendByte(0x0C, self.commandMode) # 001100 Display On,Cursor Off, Blink Off 
        self.sendByte(0x28, self.commandMode) # 101000 Data length, number of lines, font size
        self.sendByte(0x01, self.commandMode) # 000001 Clear display
        time.sleep(self.E_DELAY)
        
    # Send string to display
    def displayString(self, message, line):
        message = message.ljust(self.lcdWidth, " ")
        self.sendByte(line, self.commandMode)
        for i in range(self.lcdWidth):
            self.sendByte(ord(message[i]), self.characterMode)
            
    def clear(self):
        self.sendByte(0x01, self.commandMode)

