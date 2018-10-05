from bson.objectid import ObjectId
from waterberry.utils.logger import logger
from waterberry.utils.definition import ROOT_DIR
from waterberry.models.raspberry import Raspberry

class RaspberryDAO:
    def __init__(self, database):
        self.database = database
    
    def addRaspberries(self, raspberries):
        result = self.database.db.raspberry.insert_one(raspberries.__dict__)
        return str(result.inserted_id)

    def getRaspberryList(self):
        data = self.database.db.raspberry.find_one({})
        if data is None: return data
        raspberry_list = []
        for raspberry in data['models']: raspberry_list.append(Raspberry(**raspberry))
        return raspberry_list

    def getRasberry(self):
        data = self.database.db.raspberry.find_one({})
        if data is not None:
            models = data['models']
            raspberry = list(filter(lambda model: model['id'] == data['model'], models))[0]
            return Raspberry(**raspberry)

    def setRasberry(self, model):
        return self.database.db.raspberry.update_one({}, {"$set":  {"model": model}})