from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger
from waterberry.facade.gpio_facade import GPIOFacade
from waterberry.facade.pin_facade import PinFacade
from bson.objectid import ObjectId
import time
from datetime import datetime

def SoilSensor(electrovalve_id):
    logger.info('SoilSensor job started ...')

    with mongo.app.app_context():
        electrovalve = mongo.db.electrovalve.find_one({'_id': ObjectId(electrovalve_id)})
        sensor_pin = PinFacade(mongo).getPinIdFromName(electrovalve['sensor_pin'])

        GPIOFacade().initBoard()
        GPIOFacade().setupInputPin(sensor_pin)
        current_humidity = GPIOFacade().getPinState(sensor_pin)

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}%'
            .format(electrovalve_id, current_humidity))

        mongo.db.electrovalve.update_one({'_id': ObjectId(electrovalve_id) },
            {'$set': {'current_humidity': current_humidity}})
