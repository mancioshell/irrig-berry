from bson.objectid import ObjectId
from waterberry.utils.logger import logger
from waterberry.utils.definition import ROOT_DIR
from waterberry.models.dht_sensor import DHTSensor

class DHTSensorDAO:
    def __init__(self, database):
        self.database = database

    def addSensor(self, sensor):
        result = self.database.db.dht_sensor.insert_one(sensor.__dict__)
        sensor.id = str(result.inserted_id)
        return sensor

    def getSensor(self):
        data = self.database.db.dht_sensor.find_one({})
        if data is None: return data
        return DHTSensor(**data)

    def setSensorType(self, sensor):
        self.database.db.dht_sensor.update_one({}, {"$set":  {'type': sensor.selected}})

    def setSensorPin(self, sensor):
        self.database.db.dht_sensor.update_one({}, {"$set":  {'pin': sensor.pin}})

    def setTemperature(self, sensor):
        self.database.db.dht_sensor.update_one({}, {"$set":  {'temperature': sensor.temperature}})

    def setHumidity(self, sensor):
        self.database.db.dht_sensor.update_one({}, {"$set":  {'humidity': sensor.humidity}})    

    def getSensorData(self):
        with self.database.app.app_context():
            data = self.database.db.dht_sensor.find_one({})
            return DHTSensor(**data)
