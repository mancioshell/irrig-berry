from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger
from waterberry.facade.gpio_facade import GPIOFacade
from waterberry.facade.pin_facade import PinFacade
from bson.objectid import ObjectId
import time
from datetime import datetime

def AutomaticElectrovalve(electrovalve_id):
    with mongo.app.app_context():
        electrovalve = mongo.db.electrovalve.find_one({'_id': ObjectId(electrovalve_id)})

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}%'
            .format(electrovalve_id, electrovalve['current_humidity']))

        electrovalve_pin = PinFacade(mongo).getPinIdFromName(electrovalve['electrovalve_pin'])

        if electrovalve['current_humidity'] >= electrovalve['humidity_threshold']:
            mongo.db.electrovalve.update_one({'_id': ObjectId(electrovalve_id) },
                {'$set': {'watering': True}})

            GPIOFacade().initBoard()
            GPIOFacade().setupOutputPin(electrovalve_pin)
            GPIOFacade().enablePin(electrovalve_pin)

            logger.info('watering for ... {} seconds'.format(electrovalve['duration']))
            time.sleep(electrovalve['duration'])

            GPIOFacade().disablePin(electrovalve_pin)
            mongo.db.electrovalve.update_one({'_id': ObjectId(electrovalve_id) },
                {'$set': {'watering': False, 'last_water': datetime.utcnow()}})
