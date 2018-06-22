import time
from datetime import datetime

from waterberry.db.dao_factory import database, DaoFactory
from waterberry.gpio.soil_humidity_sensor import SoilHumiditySensor
from waterberry.gpio.board import Board
from waterberry.utils.logger import logger

def SoilSensorExecutor(electrovalve_id):
    with database.app.app_context():

        electrovalve_dao = DaoFactory().createElectrovalveDAO()
        gpio_dao = DaoFactory().createGPIODAO()
        gpio_dao.initGPIO()
        board = Board(gpio_dao)

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)

        pin_di = electrovalve['pin_di']
        pin_do = electrovalve['pin_do']
        pin_clk = electrovalve['pin_clk']
        pin_cs = electrovalve['pin_cs']

        soil_humidity_sensor = SoilHumiditySensor(board, pin_di, pin_do, pin_clk, pin_cs)
        current_humidity = soil_humidity_sensor.getData()

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}%'
            .format(electrovalve_id, current_humidity))

        electrovalve['current_humidity'] = current_humidity
        electrovalve_dao.updateElectrovalveById(electrovalve, electrovalve_id)
