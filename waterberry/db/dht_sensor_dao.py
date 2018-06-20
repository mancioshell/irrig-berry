from bson.objectid import ObjectId
from waterberry.utils.logger import logger
import os
import json
from waterberry.utils.definition import ROOT_DIR

class DHTSensorDAO:
    def __init__(self, database):
        self.database = database

    def initSensor(self):
        with self.database.app.app_context():
            result = self.database.db.dht_sensor.find_one({})
            if result is None:
                file = os.path.join(ROOT_DIR, 'data/sensor.json')
                with open(file) as f:
                    data = json.load(f)

                result = self.database.db.dht_sensor.insert_one(data)
                self.id = str(result.inserted_id)
            else:
                self.id = str(result['_id'])

    def getSensor(self):
        return self.database.db.dht_sensor.find_one({'_id': ObjectId(self.id)})

    def setSensorType(self, sensor_type):
        self.database.db.dht_sensor.update_one({'_id': ObjectId(self.id)}, {"$set":  {'type': sensor_type}})

    def setSensorPin(self, sensor_pin):
        self.database.db.dht_sensor.update_one({'_id': ObjectId(self.id)}, {"$set":  {'pin': sensor_pin}})

    def setTemperature(self, temperature):
        self.database.db.dht_sensor.update_one({'_id': ObjectId(self.id)}, {"$set":  {'temperature': temperature}})

    def setHumidity(self, humidity):
        self.database.db.dht_sensor.update_one({'_id': ObjectId(self.id)}, {"$set":  {'humidity': humidity}})

    def getTemperature(self):
        result = self.database.db.dht_sensor.find_one({'_id': ObjectId(self.id)})
        if result is not None and 'temperature' in result:
            return result['temperature']
        else:
            return None

    def getHumidity(self):
        result = self.database.db.dht_sensor.find_one({'_id': ObjectId(self.id)})
        if result is not None and 'humidity' in result:
            return result['humidity']
        else:
            return None

    def getSensorData(self):
        with self.database.app.app_context():
            return self.database.db.dht_sensor.find_one({'_id': ObjectId(self.id)})
