from src.Elevator import Elevator
from src.Arduino import Arduino

arduino = Arduino()

arduino.init()

leftElevator = Elevator(
    clawServoSlot = 0,
    id = 0,
    label = "left",
    arduinoInterface = arduino
)

leftElevator.goTo(0)