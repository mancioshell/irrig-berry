import time
from datetime import datetime

from waterberry.db.dao_factory import database, DaoFactory
from waterberry.ecomponents.dht_sensor import DHTSensor
from waterberry.models.dht_sensor import DHTSensor as DHTSensorModel
from waterberry.ecomponents.lcd import LCD
from waterberry.utils.logger import logger

def DHTSensorExecutor():
    with database.app.app_context():
        dht_sensor_dao = DaoFactory().createDHTSensorDAO()        
        raspberry_dao = DaoFactory().createRaspberryDAO()       
        lcd = LCD()

        dht_sensor = DHTSensor(dht_sensor_dao, raspberry_dao)
        humidity, temperature = dht_sensor.readData()
        lcd.writeData(humidity, temperature)

        sensor = DHTSensorModel(humidity=humidity, temperature=temperature)
        dht_sensor_dao.setHumidity(sensor)
        dht_sensor_dao.setTemperature(sensor)
