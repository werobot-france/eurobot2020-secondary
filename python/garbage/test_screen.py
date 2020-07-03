from time import sleep
from src.Scoreboard import Scoreboard

score = Scoreboard(19, 6)

while True:
    sleep(1)
    score.add()