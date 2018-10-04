from bson.objectid import ObjectId
from waterberry.utils.logger import logger
from waterberry.models.electrovalve import ElectrovalveFactory

class ElectrovalveDAO:
    def __init__(self, database):
        self.database = database       

    def getAllElectrovalves(self):
        data = list(self.database.db.electrovalve.find())
        electrovalve_list = []

        for item in data:
            electrovalve = ElectrovalveFactory(item['model']).createElectrovalve(**item)
            electrovalve_list.append(electrovalve)

        return electrovalve_list

    def getElectrovalveById(self, id):
        item = self.database.db.electrovalve.find_one({'_id': ObjectId(id)})
        return ElectrovalveFactory(item['model']).createElectrovalve(**item)

    def deleteAllElectrovalves(self):
        return self.database.db.electrovalve.remove()

    def deleteElectrovalveById(self, id):
        item = self.database.db.electrovalve.find_one_and_delete({'_id': ObjectId(id)})
        return ElectrovalveFactory(item['model']).createElectrovalve(**item)

    def createElectrovalve(self, electrovalve):
        result = self.database.db.electrovalve.insert_one(electrovalve.__dict__)
        electrovalve.id = str(result.inserted_id)
        return electrovalve

    def updateElectrovalveById(self, electrovalve):
        return self.database.db.electrovalve.update_one({'_id': ObjectId(electrovalve.id)}, {"$set":  electrovalve.__dict__})

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
