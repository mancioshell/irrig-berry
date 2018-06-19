import configparser
import os

from waterberry.utils.logger import logger

config = configparser.ConfigParser()
config.read('/media/sf_Projects/waterberry/waterberry/config/waterberry.config')
raspberry = config.getboolean(os.environ['PLATFORM'], 'RPI_GPIO')

if raspberry:
    import RPi.GPIO as GPIO

class Board:
    def __init__(self, gpio_dao):
        self.raspberry = raspberry
        self.gpio_dao = gpio_dao

    def initBoard(self):
        logger.debug('int bread board ...')
        if self.raspberry : GPIO.setwarnings(False)
        if self.raspberry : GPIO.setmode(GPIO.BCM)

    def setupOutputPin(self, pin):
        pin = self.gpio_dao.getPinByName(pin)
        logger.debug('setupOutputPin ... {}'.format(pin))
        if self.raspberry : GPIO.setup(pin, GPIO.OUT)

    def setupInputPin(self, pin):
        pin = self.gpio_dao.getPinByName(pin)
        logger.info('setupInputPin ... {}'.format(pin))
        if self.raspberry : GPIO.setup(pin, GPIO.IN)

    def enablePin(self, pin):
        pin = self.gpio_dao.getPinByName(pin)
        logger.info('enablePin ... {}'.format(pin))
        if self.raspberry : GPIO.output(pin, GPIO.LOW) # Pin on

    def disablePin(self, pin):
        pin = self.gpio_dao.getPinByName(pin)
        logger.info('disablePin ... {}'.format(pin))
        if self.raspberry : GPIO.output(pin, GPIO.HIGH) # Pin on

    def getPinState(self, pin):
        pin = self.gpio_dao.getPinByName(pin)
        if self.raspberry :
            state = GPIO.input(pin)
        else :
            state = 2
        logger.info('getPinState ... {}'.format(state))
        return state

    def cleanupPin(self, pin):
        pin = self.gpio_dao.getPinByName(pin)
        logger.info('cleanupPin ... {}'.format(pin))
        if self.raspberry : GPIO.cleanup(pin)
