from gpiozero import DigitalOutputDevice

# 21
# 10
# 9

switch = DigitalOutputDevice(10)

while True:
    print(switch.value)