from subprocess import Popen, PIPE, STDOUT

class ServoController:
    
    def __init__(self):
        self.p = Popen(
            ['python3', '/home/pi/eurobot2020-main/python/control_servo.py'],
            stdout=PIPE, 
            stdin=PIPE,
            stderr=STDOUT
        )
        print('Init done for servo controller')
    
    def setAngle(self, slot, angle):
        slot = str(slot)
        angle = str(angle)
        data = slot + ':' + angle
        print(data)
        self.p.stdin.write(bytes(data, "utf-8"))
        self.p.stdin.flush()
    