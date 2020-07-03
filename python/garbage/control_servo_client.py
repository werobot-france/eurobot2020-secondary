from subprocess import Popen, PIPE, STDOUT
from time import sleep

p = Popen(['python3', '/home/pi/eurobot2020-main/python/control_servo.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)


p.stdin.write(b"11:120\n")
p.stdin.flush()

sleep(2)

p.stdin.write(b"11:50\n")
p.stdin.flush()

sleep(2)

slot = str(11)
angle = str(110)
data = slot + ':' + angle

p.stdin.write(bytes(data, "utf-8"))
p.stdin.flush()