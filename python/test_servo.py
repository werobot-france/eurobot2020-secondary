
import Adafruit_PCA9685

driver = Adafruit_PCA9685.PCA9685()

# 75 = 0
# 510 = 180

def mappyt(x, inMin, inMax, outMin, outMax):
  return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
  

while True:
  i = int(input())
  
  driver.set_pwm(8, 0, int(mappyt(i, 0, 180, 75, 510)))
