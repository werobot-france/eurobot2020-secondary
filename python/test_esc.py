
from src.PWMDriver import PWMDriver
from src.MotorizedPlatform import MotorizedPlatform
from src.Container import Container
from time import sleep

container = Container()

driver = PWMDriver()
container.set('PWMDriver', driver)

platform = MotorizedPlatform(container)
container.set('platform', platform)

platform.stop()
sleep(2)
platform.setSpeed([
  0,
  0,
  0,
  50
])

while True:
  sleep(1)