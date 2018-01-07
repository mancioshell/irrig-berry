#import RPi.GPIO as GPIO
from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger
from bson.objectid import ObjectId
import time

class AutomaticElectrovalve:
    def __call__(self, electrovalve_id):

        with mongo.app.app_context():
            electrovalve = mongo.db.electrovalve.find_one({'_id': ObjectId(electrovalve_id) })
            logger.info('AutomaticElectrovalve job started ...')

            # GPIO.setwarnings(False)
            # GPIO.setmode(GPIO.BOARD)
            # GPIO.setup(electrovalve.electrovalve_pin, GPIO.OUT)
            #
            logger.info('Electrovalve with id  {} - Current humidity {}% : Humidity treshold {}%'
                    .format(electrovalve_id, electrovalve['current_humidity'], electrovalve['humidity_threshold']))
            if electrovalve is not None and electrovalve['current_humidity'] < electrovalve['humidity_threshold']:
                logger.info('Water electrovalve with id {} at pin {}'
                    .format(electrovalve_id, electrovalve['electrovalve_pin']))
                #     GPIO.output(electrovalve.electrovalve_pin, GPIO.LOW) # Pin on
                #     time.sleep(electrovalve.duration)
                #     GPIO.output(electrovalve.electrovalve_pin, GPIO.HIGH) # Pin off
