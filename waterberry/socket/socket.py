from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger
from waterberry.facade.gpio_facade import GPIOFacade

from bson.objectid import ObjectId
from flask_socketio import Namespace, emit
from random import randint
from threading import Lock

thread = None
thread_lock = Lock()

class ElectrovalveSocket(Namespace):

    def __init__(self, socketio):
        self.socketio = socketio
        super(ElectrovalveSocket, self).__init__()

    def __extractData(self, electrovalve):
        GPIOFacade().initBoard()
        GPIOFacade().setupInputPin(22)
        current_temperature = GPIOFacade().getPinState(22)
        current_humidity = electrovalve['current_humidity'] if 'current_humidity' in electrovalve else None
        last_water = str(electrovalve['last_water']) if 'last_water' in electrovalve else None

        return {
            '_id': str(electrovalve['_id']),
            'humidity': current_humidity,
            'temperature': current_temperature,
            'watering': electrovalve['watering'],
            'last_water': last_water
            }

    def __backgroundTask(self):
        while True:
            with mongo.app.app_context():
                electrovalves = mongo.db.electrovalve.find()
                data = map(self.__extractData, electrovalves)
                self.socketio.emit('data', data, json=True)

            self.socketio.sleep(3)

    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = self.socketio.start_background_task(target=self.__backgroundTask)

    def on_disconnect(self):
        pass
