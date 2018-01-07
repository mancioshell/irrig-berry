from waterberry.utils.logger import logger

PINS = {'GPIO_0': 11, 'GPIO_1': 12, 'GPIO_2': 13, 'GPIO_3': 15,
    'GPIO_4': 16, 'GPIO_5': 18,'GPIO_6': 22, 'GPIO_7': 7}

class PinFacade:
    def __init__(self, mongo):
        self.mongo = mongo

    def getAvailablePin(self):
        electrovalves = list(self.mongo.db.electrovalve.find())
        if electrovalves is not None:
            automatic_electrovalves = filter(lambda electrovalve: 'sensor_pin' in electrovalve, electrovalves)
            sensor_pins = map(lambda electrovalve: electrovalve['sensor_pin'], automatic_electrovalves)
            electrovalve_pins = map(lambda electrovalve: electrovalve['electrovalve_pin'], electrovalves)

            logger.info(electrovalve_pins)
            logger.info(sensor_pins)
            available_pins = [name for name, pin in PINS.iteritems()
                if name not in electrovalve_pins + sensor_pins]
            logger.info(available_pins)
            return available_pins
        else:
            return PINS

    def getAllPin(self):
        all_pins = [name for name, pin in PINS.iteritems()]
        return all_pins
