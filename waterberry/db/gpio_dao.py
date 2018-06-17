# PINS = {'GPIO_0': 11, 'GPIO_1': 12, 'GPIO_2': 13, 'GPIO_3': 15,
#     'GPIO_4': 16, 'GPIO_5': 18,'GPIO_6': 22, 'GPIO_7': 7}

PINS = {'GPIO_0': 17, 'GPIO_1': 18, 'GPIO_2': 21, 'GPIO_3': 22,
    'GPIO_4': 23, 'GPIO_5': 24,'GPIO_6': 25, 'GPIO_7': 4}

class GPIODAO:
    def __init__(self, database):
        self.database = database

    def getPinList(self):
        pin_list = [name for name, pin in PINS.iteritems()]
        return pin_list

    def getPinByName(self, name):
        return PINS[name]

    def getAvailablePinList(self):
        electrovalves = list(self.database.db.electrovalve.find())
        if electrovalves is not None:
            automatic_electrovalves = filter(lambda electrovalve: 'sensor_pin' in electrovalve, electrovalves)
            sensor_pins = map(lambda electrovalve: electrovalve['sensor_pin'], automatic_electrovalves)
            electrovalve_pins = map(lambda electrovalve: electrovalve['electrovalve_pin'], electrovalves)

            return [name for name, pin in PINS.iteritems() if name not in electrovalve_pins + sensor_pins]
        else:
            return PINS
