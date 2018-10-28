from waterberry.db.dao_factory import database
from waterberry.utils.logger import logger

from flask_socketio import Namespace, emit
from threading import Lock

thread = None
thread_lock = Lock()

class ElectrovalveSocket(Namespace):

    def __init__(self, socketio, electrovalve_dao, dht_sensor_dao):
        self.socketio = socketio
        self.electrovalve_dao = electrovalve_dao
        self.dht_sensor_dao = dht_sensor_dao
        super(ElectrovalveSocket, self).__init__()

    def __extractData(self, electrovalve):
        dht_sensor = self.dht_sensor_dao.getSensor()
        air_humidity = dht_sensor.humidity
        air_temperature = dht_sensor.temperature
        logger.info("air_humidity {} - air_temperature {}".format(air_humidity, air_temperature))

        return {
            '_id': str(electrovalve.id),
            'soil_humidity': electrovalve.current_humidity,
            'air_temperature': air_temperature,
            'air_humidity': air_humidity,
            'watering': electrovalve.watering,
            'last_water': str(electrovalve.last_water),
            'next_water': str(electrovalve.next_water)
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
