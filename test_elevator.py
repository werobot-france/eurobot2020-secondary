from src.Arduino import Arduino
#from src.Drawer import Drawer
#import Adafruit_PCA9685
from time import sleep
#from src.Elevator import Elevator
from adafruit_crickit import crickit

clawOpened = 100
clawClosed = 20

crickit.servo_2.angle = clawOpened

arduino = Arduino()

#input('>')

#crickit.servo_2.angle = clawClosed

input('>')
arduino.sendCommand(
    name = 'ELEVATOR_GO_TO',
    params = [0, 0]
)

input('>')
crickit.servo_2.angle = clawClosed

input('>')
arduino.sendCommand(
    name = 'ELEVATOR_GO_TO',
    params = [0, -425, -100]
)

# servoInterface = Adafruit_PCA9685.PCA9685()
# servoInterface.set_pwm_freq(50)

# leftElevator = Elevator(servoInterface = servoInterface, clawServoSlot = 0)
# leftElevator.openClaw()

# drawer = Drawer(servoInterface = servoInterface, squeezerServoSlot = 12)

# drawer.squeeze()
# sleep(3)

# drawer.unSqueeze()

# arduino = Arduino()
# #arduino.init()

# arduino.sendCommand(
#     name = 'DRAWER_GO_TO_BACK'
# )

# arduino.sendCommand(
#     name = 'ELEVATOR_GO_TO',
#     params = [0, 0]
# )

# input('> ')

# arduino.sendCommand(
#     name = 'ELEVATOR_GO_TO',
#     params = [0, -850, -300]
# )


# # arduino.sendCommand(
# #     name = 'ELEVATOR_GO_TO',
# #     params = [1, 0]
# # )