import Adafruit_DHT

SENSOR_TYPE_LIST = {
    'DHT11': Adafruit_DHT.DHT11,
    'DHT22': Adafruit_DHT.DHT22,
    'AM2302': Adafruit_DHT.AM2302
}

class DHTSensor:
    def __init__(self, sensor_type, pin):
        self.sensor_type = sensor_type
        self.pin = pin

    def getData(self):
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE_LIST[self.sensor_type], self.pin)
        logger.debug('getSensorData ... humidity : {} - temperature: {}'.format(humidity, temperature))
        return humidity, temperature
