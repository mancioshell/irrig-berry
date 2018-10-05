import configparser
import os

from waterberry.utils.logger import logger
from waterberry.utils.definition import ROOT_DIR

file = os.path.join(ROOT_DIR, 'config/waterberry.config')
config = configparser.ConfigParser()
config.read(file)
raspberry = config.getboolean(os.environ['PLATFORM'], 'RPI_GPIO')

if raspberry:
    import Adafruit_DHT
    SENSOR_TYPE_LIST = {
        'DHT11': Adafruit_DHT.DHT11,
        'DHT22': Adafruit_DHT.DHT22,
        'AM2302': Adafruit_DHT.AM2302
    }
else:
    SENSOR_TYPE_LIST = {
        'DHT11': 11,
        'DHT22': 22,
        'AM2302': 2302
    }


class DHTSensor:
    def __init__(self, dht_sensor_dao, raspberry_dao):
        self.raspberry = raspberry
        self.dht_sensor_dao = dht_sensor_dao
        self.raspberry_dao = raspberry_dao

    def readData(self):
        sensor_data = self.dht_sensor_dao.getSensorData()
        sensor_type = sensor_data['selected']
        pin = self.raspberry_dao.getPinByName(sensor_data['pin'])

        if self.raspberry :
            humidity, temperature = Adafruit_DHT.read(SENSOR_TYPE_LIST[sensor_type], pin)
        else:
            humidity, temperature = 2, 3
        logger.debug('getSensorData ... humidity : {} - temperature: {}'.format(humidity, temperature))
        return humidity, temperature

    def getData(self):
        return self.dht_sensor_dao.getHumidity(), self.dht_sensor_dao.getTemperature()

    def setData(self, humidity, temperature):
        self.dht_sensor_dao.setTemperature(temperature)
        self.dht_sensor_dao.setHumidity(humidity)
