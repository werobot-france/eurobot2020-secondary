from src.Arduino import Arduino
#from src.Drawer import Drawer
#import Adafruit_PCA9685
from time import sleep
#from src.Elevator import Elevator
from adafruit_crickit import crickit

clawOpened = 80
clawClosed = 20

squeezerOpened = 90
squeezerClosed = 180

crickit.servo_1.angle = squeezerOpened

crickit.servo_2.angle = clawOpened

arduino = Arduino()

input('>')

crickit.servo_1.angle = squeezerClosed

input('>')

crickit.servo_2.angle = clawClosed

# input('>DRAWER GO TO BACK')
# arduino.sendCommand(
#     name = 'DRAWER_GO_TO_BACK',
#     params = []
# )
input('>')
arduino.sendCommand(
    name = 'DRAWER_GO_TO_FRONT',
    params = []
)
input('>')
crickit.servo_1.angle = squeezerOpened

input('>')
arduino.sendCommand(
    name = 'ELEVATOR_GO_TO',
    params = [0, 0]
)

input('>')
crickit.servo_2.angle = clawOpened

input('>')

arduino.sendCommand(
    name = 'ELEVATOR_GO_TO',
    params = [0, -100, -300]
)

input('>')

crickit.servo_2.angle = clawClosed

crickit.servo_1.angle = squeezerClosed

input('>')

arduino.sendCommand(
    name = 'ELEVATOR_GO_TO',
    params = [0, -425, -100]
)

input('>')

crickit.servo_1.angle = squeezerOpened

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