from bson.objectid import ObjectId
from waterberry.utils.logger import logger
import os
import json
from waterberry.utils.definition import ROOT_DIR
from waterberry.models.raspberry import Raspberry

class RaspberryDAO:
    def __init__(self, database):
        self.database = database

    # def initGPIO(self):
    #     with self.database.app.app_context():
    #         result = self.database.db.raspberry.find_one({})
    #         if result is None:
    #             file = os.path.join(ROOT_DIR, 'data/raspberry.json')
    #             with open(file) as f:
    #                 data = json.load(f)
    #             result = self.database.db.raspberry.insert_one(data)
    #             self.id = str(result.inserted_id)
    #         else:
    #             self.id = str(result['_id'])

    def getRaspberryList(self):
        data = self.database.db.raspberry.find_one({})
        raspberry_list = []
        for raspberry in data['models']: raspberry_list.append(Raspberry(**raspberry))
        return raspberry_list

    def addRaspberry(self, raspberry):
        result = self.database.db.raspberry.insert_one(raspberry.__dict__)
        return str(result.inserted_id)

    def getRasberry(self):
        data = self.database.db.raspberry.find_one({})
        raspberry = filter(lambda model: model['id'] == data['model'], data['models'])[0]
        return Raspberry(**raspberry)

    def setRasberry(self, model):
        return self.database.db.raspberry.update_one({}, {"$set":  {"model": model}})

    # def getRaspberryModelList(self):
    #     raspberry = self.database.db.raspberry.find_one({'_id': ObjectId(self.id)})
    #     return raspberry
    #
    # def setRaspberryPiModel(self, model):
    #     return self.database.db.raspberry.update_one({'_id': ObjectId(self.id)}, {"$set":  {"model": model}})
    #
    # def getPinList(self):
    #     raspberry = self.database.db.raspberry.find_one({'_id': ObjectId(self.id)})
    #     pins = filter(lambda model: model['id'] == raspberry['model'], raspberry['models'])[0]['gpio']
    #     pin_list = [name for name, pin in pins.iteritems()]
    #     return pin_list
    #
    # def getPinByName(self, name):
    #     raspberry = self.database.db.raspberry.find_one({'_id': ObjectId(self.id)})
    #     pins = filter(lambda model: model['id'] == raspberry['model'], raspberry['models'])[0]['gpio']
    #     return pins[name]

    # def getAvailablePinList(self, electrovalves, dht_sensor_pin):
    #     raspberry = self.database.db.raspberry.find_one({'_id': ObjectId(self.id)})
    #     pins = filter(lambda model: model['id'] == raspberry['model'], raspberry['models'])[0]['gpio']
    #
    #     filter_automatic_electrovalve = lambda electrovalve: electrovalve['mode'] == 'automatic'
    #     map_automatic_pin = lambda electrovalve: [electrovalve['pin_di'],
    #         electrovalve['pin_do'], electrovalve['pin_clk'], electrovalve['pin_cs']]
    #     reduce_pin_list = lambda list1, list2: list1+list2
    #
    #     if electrovalves is not None:
    #         automatic_electrovalves = filter(filter_automatic_electrovalve, electrovalves)
    #         logger.info(automatic_electrovalves)
    #
    #         sensor_pins = reduce(reduce_pin_list, map(map_automatic_pin, automatic_electrovalves), [])
    #         electrovalve_pins = map(lambda electrovalve: electrovalve['electrovalve_pin'], electrovalves)
    #
    #         return [name for name, pin in pins.iteritems() if name not in electrovalve_pins + sensor_pins + [dht_sensor_pin]]
    #     else:
    #         return pins
