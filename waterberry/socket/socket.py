from waterberry.db.pymongo import mongo
from waterberry.utils.logger import logger

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

    def background_thread(self):
        while True:
            current_temperature = randint(5, 40);

            def extract_data(electrovalve):
                if 'current_humidity' in electrovalve:
                    current_humidity = electrovalve['current_humidity']
                else:
                    current_humidity = None

                if 'last_water'  in electrovalve:
                    last_water = str(electrovalve['last_water'])
                else:
                    last_water = None

                if electrovalve['mode'] == 'automatic':
                    return {'_id': str(electrovalve['_id']),
                        'humidity': current_humidity,
                        'temperature': current_temperature,
                        'watering': electrovalve['watering'],
                        'last_water': last_water}
                else:
                    return {'_id': str(electrovalve['_id']),
                        'humidity': None,
                        'temperature': current_temperature,
                        'watering': electrovalve['watering'],
                        'last_water': last_water}

            with mongo.app.app_context():
                electrovalves = mongo.db.electrovalve.find()
                data = map(extract_data, electrovalves)
                self.socketio.emit('data', data, json=True)

            self.socketio.sleep(3)

    def on_connect(self):
        logger.error("connect ...")

        global thread
        with thread_lock:
            if thread is None:
                thread = self.socketio.start_background_task(target=self.background_thread)

    def on_disconnect(self):
        logger.info("disconnect ...")
        pass
