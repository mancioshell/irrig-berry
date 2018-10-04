import time
from datetime import datetime

from waterberry.db.dao_factory import database, DaoFactory
from waterberry.ecomponents.board import Board
from waterberry.utils.logger import logger

def ManualElectrovalveExecutor(electrovalve_id):
    with database.app.app_context():
        electrovalve_dao = DaoFactory().createElectrovalveDAO()
        raspberry_dao = DaoFactory().createRaspberryDAO()        
        board = Board()
        raspberry = raspberry_dao.getRasberry()

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)        

        logger.info('ManualElectrovalveExecutor job started ...')
        logger.info('Water electrovalve with id {} at pin {}'.format(electrovalve_id, electrovalve.getUsedPins()))

        electrovalve.watering = True
        electrovalve_dao.updateElectrovalveById(electrovalve)
        pin = raspberry.getPinByName(electrovalve.getUsedPins())

        board.initBoard()
        board.setupOutputPin(pin)
        board.enablePin(pin)

        logger.info('watering for ... {} seconds'.format(electrovalve['duration']))
        time.sleep(electrovalve['duration'])

        board.disablePin(pin)
        electrovalve.watering = False
        electrovalve.last_water = datetime.utcnow()
        electrovalve_dao.updateElectrovalveById(electrovalve)
