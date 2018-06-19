from bson.objectid import ObjectId
from waterberry.utils.logger import logger

DEFAULT_PINS = {
    'GPIO_0': 17, 'GPIO_1': 18, 'GPIO_2': 21, 'GPIO_3': 22,
    'GPIO_4': 23, 'GPIO_5': 24,'GPIO_6': 25, 'GPIO_7': 4
}

class GPIODAO:
    def __init__(self, database):
        self.database = database

    def initGPIO(self, pins=DEFAULT_PINS):
        with self.database.app.app_context():
            result = self.database.db.gpio.find_one({})
            if result is None:
                result = self.database.db.gpio.insert_one({'pins': pins})
                self.id = str(result.inserted_id)
            else:
                self.id = str(result['_id'])

    def getPinList(self):
        pins = self.database.db.gpio.find_one({'_id': ObjectId(self.id)})
        pin_list = [name for name, pin in pins['pins'].iteritems()]
        return pin_list

    def getPinByName(self, name):
        pins = self.database.db.gpio.find_one({'_id': ObjectId(self.id)})
        logger.info('pins')
        logger.info(pins)
        logger.info('name')
        logger.info(name)
        return pins['pins'][name]

    def getAvailablePinList(self, electrovalves):
        pins = self.database.db.gpio.find_one({'_id': ObjectId(self.id)})

        filter_automatic_electrovalve = lambda electrovalve: electrovalve['mode'] == 'automatic'
        map_automatic_pin = lambda electrovalve: [electrovalve['pin_di'],
            electrovalve['pin_do'], electrovalve['pin_clk'], electrovalve['pin_cs']]
        reduce_pin_list = lambda list1, list2: list1+list2

        if electrovalves is not None:
            automatic_electrovalves = filter(filter_automatic_electrovalve, electrovalves)
            logger.info(automatic_electrovalves)

            sensor_pins = reduce(reduce_pin_list, map(map_automatic_pin, automatic_electrovalves), [])
            electrovalve_pins = map(lambda electrovalve: electrovalve['electrovalve_pin'], electrovalves)

            return [name for name, pin in pins['pins'].iteritems() if name not in electrovalve_pins + sensor_pins]
        else:
            return pins['pins']
