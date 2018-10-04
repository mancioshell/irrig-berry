import time
from datetime import datetime

from waterberry.db.dao_factory import database, DaoFactory
from waterberry.ecomponents.board import Board
from waterberry.utils.logger import logger

def AutomaticElectrovalveExecutor(electrovalve_id):
    with database.app.app_context():
        electrovalve_dao = DaoFactory().createElectrovalveDAO()
        raspberry_dao = DaoFactory().createRaspberryDAO()
        raspberry = raspberry_dao.getRasberry()

        board = Board()

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}% \with the humidity threshold {}%'
            .format(electrovalve_id, electrovalve.current_humidity, electrovalve.humidity_threshold))

        if electrovalve.current_humidity <= electrovalve.humidity_threshold:
            electrovalve.watering = True
            electrovalve_dao.updateElectrovalveById(electrovalve)
            board.initBoard()
            pin = raspberry.getPinByName(electrovalve.getUsedPins())           
            board.setupOutputPin(pin)
            board.enablePin(pin)

            logger.info('watering for ... {} seconds'.format(electrovalve.duration))
            time.sleep(electrovalve.duration)

            board.disablePin(pin)
            electrovalve.watering = False
            electrovalve.last_water = datetime.utcnow()
            electrovalve_dao.updateElectrovalveById(electrovalve)
