import configparser
import os

from waterberry.utils.logger import logger
from waterberry.utils.definition import ROOT_DIR

file = os.path.join(ROOT_DIR, 'config/waterberry.config')
config = configparser.ConfigParser()
config.read(file)
raspberry = config.getboolean(os.environ['PLATFORM'], 'RPI_GPIO')

if raspberry:
    import RPi.GPIO as GPIO

class Board:
    def __init__(self, raspberry_dao):
        self.raspberry = raspberry

    def initBoard(self):
        logger.debug('int bread board ...')
        if self.raspberry : GPIO.setwarnings(False)
        if self.raspberry : GPIO.setmode(GPIO.BCM)

    def setupOutputPin(self, pin):
        logger.debug('setupOutputPin ... {}'.format(pin))
        if self.raspberry : GPIO.setup(pin, GPIO.OUT)

    def setupInputPin(self, pin):
        logger.info('setupInputPin ... {}'.format(pin))
        if self.raspberry : GPIO.setup(pin, GPIO.IN)

    def enablePin(self, pin):
        logger.info('enablePin ... {}'.format(pin))
        if self.raspberry : GPIO.output(pin, GPIO.LOW) # Pin on

    def disablePin(self, pin):
        logger.info('disablePin ... {}'.format(pin))
        if self.raspberry : GPIO.output(pin, GPIO.HIGH) # Pin on

    def getPinState(self, pin):
        if self.raspberry :
            state = GPIO.input(pin)
        else :
            state = 2
        logger.info('getPinState ... {}'.format(state))
        return state

    def cleanupPin(self, pin):
        logger.info('cleanupPin ... {}'.format(pin))
        if self.raspberry : GPIO.cleanup(pin)