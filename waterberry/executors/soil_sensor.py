import time
from datetime import datetime

from waterberry.db.dao_factory import database, DaoFactory
from waterberry.ecomponents.soil_humidity_sensor import SoilHumiditySensor
from waterberry.ecomponents.board import Board
from waterberry.utils.logger import logger

def SoilSensorExecutor(electrovalve_id):
    with database.app.app_context():

        electrovalve_dao = DaoFactory().createElectrovalveDAO()
        raspberry_dao = DaoFactory().createRaspberryDAO()
        raspberry_dao.initGPIO()
        board = Board(raspberry_dao)

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)

        pin_di = raspberry_dao.getPinByName(electrovalve['pin_di'])
        pin_do = raspberry_dao.getPinByName(electrovalve['pin_do'])
        pin_clk = raspberry_dao.getPinByName(electrovalve['pin_clk'])
        pin_cs = raspberry_dao.getPinByName(electrovalve['pin_cs'])

        soil_humidity_sensor = SoilHumiditySensor(board, pin_di, pin_do, pin_clk, pin_cs)
        current_humidity = soil_humidity_sensor.getData()

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}%'
            .format(electrovalve_id, current_humidity))

        electrovalve['current_humidity'] = current_humidity
        electrovalve_dao.updateElectrovalveById(electrovalve, electrovalve_id)
