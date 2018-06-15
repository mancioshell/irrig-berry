from flask_pymongo import PyMongo
from waterberry.utils.logger import logger
from waterberry.db.electrovalve_dao import ElectrovalveDAO
from waterberry.db.gpio_dao import GPIODAO
from waterberry.db.dht_sensor_dao import DHTSensorDAO

MONGO_HOST = '10.0.2.15'
MONGO_PORT = 27017
MONGO_DBNAME = 'waterberry_db'
database = PyMongo()

class DaoFactory:
    def __init__(self):
        pass

    def initApp(self, app):
        app.config['MONGO_HOST'] = MONGO_HOST
        app.config['MONGO_PORT'] = MONGO_PORT
        app.config["MONGO_DBNAME"] = MONGO_DBNAME
        database.init_app(app, config_prefix='MONGO')
        database.app = app
        return app

    def createElectrovalveDAO(self):
        return ElectrovalveDAO(database)

    def createGPIODAO(self):
        return GPIODAO(database)

    def createDHTSensorDAO(self):
        return DHTSensorDAO(database)
