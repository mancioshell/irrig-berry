#import RPi.GPIO as GPIO
from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger
from bson.objectid import ObjectId
import time
from random import randint

#'current_humidity': { '$gte': 2 }

class SoilSensor:
    def __call__(self, electrovalve_id):
        logger.info('SoilSensor job started ...')
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(pin, GPIO.IN)
        current_humidity = randint(1, 100);
        with mongo.app.app_context():
            logger.info('Soil sensor for electrovalve with id {} has observed humidity {}%'
                .format(electrovalve_id, current_humidity))
            mongo.db.electrovalve.find_one_and_update({'_id': ObjectId(electrovalve_id) },
                {'$set': {'current_humidity': current_humidity}})
