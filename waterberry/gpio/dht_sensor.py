import configparser
import os

from waterberry.utils.logger import logger

config = configparser.ConfigParser()
config.read('config/waterberry.config')
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
    def __init__(self, dht_sensor_dao, gpio_dao):
        self.raspberry = raspberry
        self.dht_sensor_dao = dht_sensor_dao
        self.gpio_dao = gpio_dao

    def readData(self):
        sensor_data = self.dht_sensor_dao.getSensorData()
        sensor_type = sensor_data['type']
        pin = self.gpio_dao.getPinByName(sensor_data['pin'])

        if self.raspberry :
            humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE_LIST[sensor_type], pin)
        else:
            humidity, temperature = 2, 3
        logger.debug('getSensorData ... humidity : {} - temperature: {}'.format(humidity, temperature))
        return humidity, temperature

    def getData(self):
        return self.dht_sensor_dao.getTemperature()
        return self.dht_sensor_dao.getHumidity()

    def setData(self, humidity, temperature):
        self.dht_sensor_dao.setTemperature(temperature)
        self.dht_sensor_dao.setHumidity(humidity)
