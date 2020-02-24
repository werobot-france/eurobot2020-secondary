from src.Arduino import Arduino
from time import sleep

arduino = Arduino()

arduino.init()

sleep(2)
arduino.sendCommand(
    name = 'CMD',
    params = [255, -2, 30],
    expectResponse = True
)