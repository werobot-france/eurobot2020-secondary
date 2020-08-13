
from time import sleep
from src.Logger import LoggerManager

manager = LoggerManager()

logger = manager.get('Arduino')

logger.debug('Hey!')
logger.info('Hey!')
logger.warn('Hey!')
logger.error('Hey!')