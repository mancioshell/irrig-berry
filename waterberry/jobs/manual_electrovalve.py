from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger
from waterberry.facade.gpio_facade import GPIOFacade
from waterberry.facade.pin_facade import PinFacade
from bson.objectid import ObjectId
import time
from datetime import datetime

def ManualElectrovalve(electrovalve_id):
    with mongo.app.app_context():
        electrovalve = mongo.db.electrovalve.find_one({'_id': ObjectId(electrovalve_id)})

        electrovalve_pin = PinFacade(mongo).getPinIdFromName(electrovalve['electrovalve_pin'])

        logger.info('ManualElectrovalve job started ...')
        logger.info('Water electrovalve with id {} at pin {}'
            .format(electrovalve_id, electrovalve_pin))

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
