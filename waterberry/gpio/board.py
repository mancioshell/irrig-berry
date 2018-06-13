#import RPi.GPIO as GPIO
#import Adafruit_DHT

from waterberry.utils.logger import logger

#SENSOR_TYPE = Adafruit_DHT.DHT11
SENSOR_TYPE = 11
TEMP_HUMIDITY_PIN = 22

class Board:
    def __init__(self):
        pass

    def initBoard(self):
        logger.debug('int bread board ...')
        #GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)

    def getSensorData(self):
        #humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, TEMP_HUMIDITY_PIN)
        humidity, temperature = 2, 3
        logger.debug('getSensorData ... humidity : {} - temperature: {}'.format(humidity, temperature))
        return humidity, temperature

    def setupOutputPin(self, pin):
        logger.debug('setupOutputPin ... {}'.format(pin))
        #GPIO.setup(pin, GPIO.OUT)

    def setupInputPin(self, pin):
        logger.info('setupInputPin ... {}'.format(pin))
        #GPIO.setup(pin, GPIO.IN)

    def enablePin(self, pin):
        logger.info('enablePin ... {}'.format(pin))
        #GPIO.output(pin, GPIO.LOW) # Pin on

    def disablePin(self, pin):
        logger.info('disablePin ... {}'.format(pin))
        #GPIO.output(pin, GPIO.HIGH) # Pin on

    def getPinState(self, pin):
        #state = GPIO.input(pin)
        state = 2
        logger.info('getPinState ... {}'.format(state))
        return state

    def cleanupPin(self, pin):
        logger.info('cleanupPin ... {}'.format(pin))
        #GPIO.cleanup(pin)