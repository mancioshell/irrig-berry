import RPi.GPIO as GPIO

from waterberry.utils.logger import logger

class Board:
    def __init__(self):
        pass

    def initBoard(self):
        logger.debug('int bread board ...')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def setupOutputPin(self, pin):
        logger.debug('setupOutputPin ... {}'.format(pin))
        GPIO.setup(pin, GPIO.OUT)

    def setupInputPin(self, pin):
        logger.info('setupInputPin ... {}'.format(pin))
        GPIO.setup(pin, GPIO.IN)

    def enablePin(self, pin):
        logger.info('enablePin ... {}'.format(pin))
        GPIO.output(pin, GPIO.LOW) # Pin on

    def disablePin(self, pin):
        logger.info('disablePin ... {}'.format(pin))
        GPIO.output(pin, GPIO.HIGH) # Pin on

    def getPinState(self, pin):
        state = GPIO.input(pin)
        logger.info('getPinState ... {}'.format(state))
        return state

    def cleanupPin(self, pin):
        logger.info('cleanupPin ... {}'.format(pin))
        GPIO.cleanup(pin)
