import time
from datetime import datetime

from waterberry.db.dao_factory import database, DaoFactory
from waterberry.gpio.board import Board
from waterberry.utils.logger import logger

def SoilSensor(electrovalve_id):
    with database.app.app_context():

        electrovalve_dao = DaoFactory().createElectrovalveDAO()
        gpio_dao = DaoFactory().createGPIODAO()
        board = Board()

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)
        sensor_pin = gpio_dao.getPinByName(electrovalve['sensor_pin'])

        board.initBoard()
        board.setupInputPin(sensor_pin)
        current_humidity = board.getPinState(sensor_pin)

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}%'
            .format(electrovalve_id, current_humidity))

        electrovalve['current_humidity'] = current_humidity
        electrovalve_dao.updateElectrovalveById(electrovalve, electrovalve_id)
