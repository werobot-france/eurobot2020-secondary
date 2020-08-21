from math import *
from ..API import API

class Goblol(API):
  
  def run(self):
    #self.navigation.orientTo(pi)
    # self.navigation.goTo(x=200, y=950, theta=pi)
    # input('?')
    # self.navigation.goTo(x=-500, y=950, theta=pi, stopOn='front')
    
    
    # 1. Elevator go to TOP
    self.navigation.goTo(x=829, y=159, theta=pi)
    self.navigation.goTo(x=829, y=700, theta=pi)
    self.navigation.goTo(x=300, y=700, theta=pi)
    self.navigation.goTo(x=300, y=975, theta=pi)
    self.navigation.goTo(x=200, y=975, theta=pi)
    #self.navigation.goTo(x=770, y=1000, theta=pi)