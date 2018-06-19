import configparser
import os

from flask_pymongo import PyMongo
from waterberry.utils.logger import logger
from waterberry.db.electrovalve_dao import ElectrovalveDAO
from waterberry.db.gpio_dao import GPIODAO
from waterberry.db.dht_sensor_dao import DHTSensorDAO

config = configparser.ConfigParser()
config.read('/media/sf_Projects/waterberry/waterberry/config/waterberry.config')

database = PyMongo()

class DaoFactory:
    def __init__(self):
        self.configuration = os.environ['PLATFORM']

    def initApp(self, app):
        app.config['MONGO_HOST'] = config.get(self.configuration, 'MONGO_HOST')
        app.config['MONGO_PORT'] = config.getint(self.configuration, 'MONGO_PORT')
        app.config["MONGO_DBNAME"] = config.get(self.configuration, 'MONGO_DBNAME')
        database.init_app(app, config_prefix='MONGO')
        database.app = app
        return app

    def createElectrovalveDAO(self):
        return ElectrovalveDAO(database)

    def createGPIODAO(self):
        return GPIODAO(database)

    def createDHTSensorDAO(self):
        return DHTSensorDAO(database)
