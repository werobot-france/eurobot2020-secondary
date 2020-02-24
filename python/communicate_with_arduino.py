from src.Arduino import Arduino

arduino = Arduino()

arduino.init()

arduino.sendCommand(
    name = 'CMD',
    params = [255, -2, 30],
    expectResponse = True
)