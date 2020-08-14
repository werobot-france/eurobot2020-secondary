
from time import sleep
from src.Logger import LoggerManager
from math import *

manager = LoggerManager()
manager.setLevel('debug')

logger = manager.get('Arduino')

logger.debug('Hey! ' + logger.data({'x': pi/2, 'y': pi/4}))
logger.debug('Hey!')
logger.info('Hey!')
logger.warn('Hey!')
logger.error('Hey!')

