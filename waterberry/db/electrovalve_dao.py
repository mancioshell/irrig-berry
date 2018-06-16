from bson.objectid import ObjectId
from waterberry.utils.logger import logger

class ElectrovalveDAO:
    def __init__(self, database):
        self.database = database

    def getElectrovalveList(self):
        return list(self.database.db.electrovalve.find())

    def deleteElectrovalveList(self):
        return self.database.db.electrovalve.remove()

    def getElectrovalveById(self, id):
        return self.database.db.electrovalve.find_one({'_id': ObjectId(id)})

    def createElectrovalve(self, electrovalve):
        electrovalve['watering'] = False
        return self.database.db.electrovalve.insert_one(electrovalve)

    def updateElectrovalveById(self, electrovalve, id):
        if electrovalve['mode'] == 'automatic':
            electrovalve['timetable'] = None
        elif electrovalve['mode'] == 'scheduled':
            electrovalve['humidity_threshold'] = None
            electrovalve['sensor_pin'] = None
        else:
            electrovalve['timetable'] = None
            electrovalve['humidity_threshold'] = None
            electrovalve['sensor_pin'] = None

        logger.error(electrovalve)       
        return self.database.db.electrovalve.update_one({'_id': ObjectId(id)}, {"$set":  electrovalve})

    def deleteElectrovalveById(self, id):
        return self.database.db.electrovalve.find_one_and_delete({'_id': ObjectId(id)})
