from waterberry.db.dao_factory import database
from waterberry.utils.logger import logger

from flask_socketio import Namespace, emit
from threading import Lock

thread = None
thread_lock = Lock()

class ElectrovalveSocket(Namespace):

    def __init__(self, socketio, electrovalve_dao, dht_sensor):
        self.socketio = socketio
        self.electrovalve_dao = electrovalve_dao
        self.dht_sensor = dht_sensor
        super(ElectrovalveSocket, self).__init__()

    def __extractData(self, electrovalve):
        air_humidity, air_temperature = self.dht_sensor.getData()
        logger.info("air_humidity {} - air_temperature {}".format(air_humidity, air_temperature))
        current_humidity = electrovalve['current_humidity'] if 'current_humidity' in electrovalve else None
        last_water = str(electrovalve['last_water']) if 'last_water' in electrovalve else None
        next_water = str(electrovalve['next_water']) if 'next_water' in electrovalve else None

        return {
            '_id': str(electrovalve['_id']),
            'soil_humidity': current_humidity,
            'air_temperature': air_temperature,
            'air_humidity': air_humidity,
            'watering': electrovalve['watering'],
            'last_water': last_water,
            'next_water': next_water
            }

    def __backgroundTask(self):
        while True:
            with database.app.app_context():
                electrovalves = self.electrovalve_dao.getElectrovalveList()
                data = map(self.__extractData, electrovalves)
                self.socketio.emit('data', data, json=True)

            self.socketio.sleep(5)

    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = self.socketio.start_background_task(target=self.__backgroundTask)

    def on_disconnect(self):
        pass
