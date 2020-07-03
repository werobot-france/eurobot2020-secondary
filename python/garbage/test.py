from src.Stepper import Stepper
from math import degrees
from time import sleep
import sys
import os

# stepper A du coté des ports ethernet et USB
stepperA = Stepper(directionPin=26, stepPin=19, sleepPin=13)
stepperB = Stepper(directionPin=6, stepPin=5, sleepPin=0, endSwitchPin=21, originDirectionIsClockwise=True)
stepperC = Stepper(directionPin=17, stepPin=27, sleepPin=22)

stepper = stepperB

def main():
    stepper.goToOrigin()
    #stepper.setAnticlockwise() # elevator = vers le haut
    # stepper.setClockwise()
    # stepper.enable()
    # stepper.move(200, 0.4)
    
    # stepper.disable()
    #while True:
        
        # print('Stop')
        # sleep(0.5)
        # print('Replay')
        # stepper.setAnticlockwise()
        # stepper.move(300, 1.3)
        # #stepper.disable()
        # print(degrees(stepper.getPosition()) % 360)
        #sleep(1)

    while True:
        sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        stepper.disable()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
