import configparser
import os

from waterberry.utils.logger import logger
from waterberry.utils.definition import ROOT_DIR
from waterberry.db.raspberry_dao import RaspberryDAO
from waterberry.db.dht_sensor_dao import DHTSensorDAO

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
        sensor = self.dht_sensor_dao.getSensorData()
        sensor_type = sensor.selected
        rasperry = self.raspberry_dao.getRasberry()
        pin = rasperry.getPinByName(sensor.pin)

        if self.raspberry :
            humidity, temperature = Adafruit_DHT.read(SENSOR_TYPE_LIST[sensor_type], pin)
        else:
            humidity, temperature = 2, 3
        logger.debug('getSensorData ... humidity : {} - temperature: {}'.format(humidity, temperature))
        return humidity, temperature
