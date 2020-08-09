from math import *
from ..API import API

class TestScript(API):
  
  def run(self):
    self.navigation.orientTo(pi)
    #self.navigation.goTo(x=10, y=10, theta=pi)