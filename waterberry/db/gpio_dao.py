from bson.objectid import ObjectId
from waterberry.utils.logger import logger
import os
import json
from waterberry.utils.definition import ROOT_DIR

class GPIODAO:
    def __init__(self, database):
        self.database = database

    def initGPIO(self):
        with self.database.app.app_context():
            result = self.database.db.gpio.find_one({})
            if result is None:
                file = os.path.join(ROOT_DIR, 'data/raspberry.json')
                with open(file) as f:
                    data = json.load(f)
                result = self.database.db.gpio.insert_one(data)
                self.id = str(result.inserted_id)
            else:
                self.id = str(result['_id'])

    def getRaspberryModelList(self):
        raspberry = self.database.db.gpio.find_one({'_id': ObjectId(self.id)})
        return raspberry

    def setRaspberryPiModel(self, model):
        return self.database.db.gpio.update_one({'_id': ObjectId(self.id)}, {"$set":  {"model": model}})

    def getPinList(self):
        raspberry = self.database.db.gpio.find_one({'_id': ObjectId(self.id)})
        pins = filter(lambda model: model['id'] == raspberry['model'], raspberry['models'])[0]['gpio']
        pin_list = [name for name, pin in pins.iteritems()]
        return pin_list

    def getPinByName(self, name):
        raspberry = self.database.db.gpio.find_one({'_id': ObjectId(self.id)})
        pins = filter(lambda model: model['id'] == raspberry['model'], raspberry['models'])[0]['gpio']
        return pins[name]

    def getAvailablePinList(self, electrovalves):
        raspberry = self.database.db.gpio.find_one({'_id': ObjectId(self.id)})
        pins = filter(lambda model: model['id'] == raspberry['model'], raspberry['models'])[0]['gpio']

        filter_automatic_electrovalve = lambda electrovalve: electrovalve['mode'] == 'automatic'
        map_automatic_pin = lambda electrovalve: [electrovalve['pin_di'],
            electrovalve['pin_do'], electrovalve['pin_clk'], electrovalve['pin_cs']]
        reduce_pin_list = lambda list1, list2: list1+list2

        if electrovalves is not None:
            automatic_electrovalves = filter(filter_automatic_electrovalve, electrovalves)
            logger.info(automatic_electrovalves)

            sensor_pins = reduce(reduce_pin_list, map(map_automatic_pin, automatic_electrovalves), [])
            electrovalve_pins = map(lambda electrovalve: electrovalve['electrovalve_pin'], electrovalves)

            return [name for name, pin in pins.iteritems() if name not in electrovalve_pins + sensor_pins]
        else:
            return pins
