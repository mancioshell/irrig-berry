from bson.objectid import ObjectId
from waterberry.utils.logger import logger

from waterberry.models.electrovalve import ManualElectrovalve
from waterberry.models.electrovalve import AutomaticElectrovalve
from waterberry.models.electrovalve import ScheduledElectrovalve

class ElectrovalveDAO:
    def __init__(self, database, electrovalve_factory):
        self.database = database
        self.electrovalve_factory = electrovalve_factory

    def getAllElectrovalves(self):
        data = list(self.database.db.electrovalve.find())
        electrovalve_list = []

        for item in data:
            electrovalve = self.electrovalve_factory.createElectrovalve(item)
            electrovalve_list.append(electrovalve)

        return electrovalve_list

    def getElectrovalveById(self, id):
        item = self.database.db.electrovalve.find_one({'_id': ObjectId(id)})
        return self.electrovalve_factory.createElectrovalve(item)

    def deleteAllElectrovalve(self):
        return self.database.db.electrovalve.remove()

    def deleteElectrovalveById(self, id):
        return self.database.db.electrovalve.find_one_and_delete({'_id': ObjectId(id)})

    def createElectrovalve(self, electrovalve):
        return self.database.db.electrovalve.insert_one(electrovalve.__dict__)

    def updateElectrovalveById(self, electrovalve):
        return self.database.db.electrovalve.update_one({'_id': ObjectId(id)}, {"$set":  electrovalve.__dict__})

    # def updateElectrovalveById(self, electrovalve, id):
    #     if electrovalve['mode'] == 'automatic':
    #         electrovalve['timetable'] = None
    #     elif electrovalve['mode'] == 'scheduled':
    #         electrovalve['humidity_threshold'] = None
    #         electrovalve['pin_di'] = None
    #         electrovalve['pin_do'] = None
    #         electrovalve['pin_clk'] = None
    #         electrovalve['pin_cs'] = None
    #     else:
    #         electrovalve['timetable'] = None
    #         electrovalve['humidity_threshold'] = None
    #         electrovalve['pin_di'] = None
    #         electrovalve['pin_do'] = None
    #         electrovalve['pin_clk'] = None
    #         electrovalve['pin_cs'] = None
    #
    #     logger.info(electrovalve)
    #     electrovalve.pop('_id', None)
    #     return self.database.db.electrovalve.update_one({'_id': ObjectId(id)}, {"$set":  electrovalve})
