from bson.objectid import ObjectId
from waterberry.utils.logger import logger

SENSOR_TYPE_LIST = ['DHT11', 'DHT22', 'AM2302']

class DHTSensorDAO:
    def __init__(self, database):
        self.database = database

    def initSensor(self, type='DHT11', pin='GPIO_6'):
        with self.database.app.app_context():
            result = self.database.db.dht_sensor.find_one({})
            if result is None:
                result = self.database.db.dht_sensor.insert_one({'type': type, 'pin' : pin})
                self.id = str(result.inserted_id)
            else:
                self.id = str(result['_id'])

    def getSensorTypeList(self):
        return SENSOR_TYPE_LIST

    def getSensor(self):
        return self.database.db.dht_sensor.find_one({'_id': ObjectId(self.id)})

    def setSensorType(self, sensor_type):
        self.database.db.dht_sensor.update_one({'_id': ObjectId(self.id)}, {"$set":  {'type': sensor_type}})

    def setSensorPin(self, sensonr_pin):
        self.database.db.dht_sensor.update_one({'_id': ObjectId(self.id)}, {"$set":  {'pin': sensonr_pin}})

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
        if result is not None and 'humidity' in result:
            return result['humidity']
        else:
            return None

    def getSensorData(self):
        with self.database.app.app_context():
            return self.database.db.dht_sensor.find_one({'_id': ObjectId(self.id)})
