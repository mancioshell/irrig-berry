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
        raspberry = raspberry_dao.getRasberry()
        board = Board()

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)
        used_pins = raspberry.getPinByName(electrovalve.getUsedPins())   

        soil_humidity_sensor = SoilHumiditySensor(board, **used_pins)
        current_humidity = soil_humidity_sensor.getData()

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}%'
            .format(electrovalve_id, current_humidity))

        electrovalve.current_humidity = current_humidity
        electrovalve_dao.updateElectrovalveById(electrovalve)
