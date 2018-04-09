import RPi.GPIO as GPIO

from waterberry.utils.logger import logger
from random import randint

class GPIOFacade:

    def initBoard(self):
        logger.info('int bread board ...')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def setupOutputPin(self, pin):
        logger.info('setupOutputPin ... {}'.format(pin))
        GPIO.setup(pin, GPIO.OUT)

    def setupInputPin(self, pin):
        logger.info('setupInputPin ... {}'.format(pin))
        GPIO.setup(pin, GPIO.IN)

    def getPinState(self, pin):
        logger.info('getPinState ... {}'.format(pin))
        return GPIO.input(pin)

    def enablePin(self, pin):
        logger.info('enablePin ... {}'.format(pin))
        GPIO.output(pin, GPIO.LOW) # Pin on

    def disablePin(self, pin):
        logger.info('disablePin ... {}'.format(pin))
        GPIO.output(pin, GPIO.HIGH) # Pin on

    def cleanupPin(self, pin):
        logger.info('cleanupPin ... {}'.format(pin))
        GPIO.cleanup(pin)
