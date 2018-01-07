#import RPi.GPIO as GPIO
from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger
from bson.objectid import ObjectId
import time
from datetime import datetime

class ManualElectrovalve:
    def __call__(self, electrovalve_id):

        with mongo.app.app_context():
            electrovalve = mongo.db.electrovalve.find_one_and_update({'_id': ObjectId(electrovalve_id) },
            {'$set': {'watering': True}})
            logger.info('ManualElectrovalve job started ...')
            logger.info('Water electrovalve with id {} at pin {}'
                .format(electrovalve_id, electrovalve['electrovalve_pin']))
            time.sleep(electrovalve['duration'])
            electrovalve = mongo.db.electrovalve.find_one_and_update({'_id': ObjectId(electrovalve_id) },
            {'$set': {'watering': False, 'last_water': datetime.utcnow()}})

            # GPIO.setwarnings(False)
            # GPIO.setmode(GPIO.BOARD)
            # GPIO.setup(electrovalve.electrovalve_pin, GPIO.OUT)
            # GPIO.output(electrovalve.electrovalve_pin, GPIO.LOW) # Pin on
            # time.sleep(electrovalve.duration)
            # GPIO.output(electrovalve.electrovalve_pin, GPIO.HIGH) # Pin off
