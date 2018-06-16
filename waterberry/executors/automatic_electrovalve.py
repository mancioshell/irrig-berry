import time
from datetime import datetime

from waterberry.db.dao_factory import database, DaoFactory
from waterberry.gpio.board import Board
from waterberry.utils.logger import logger

def AutomaticElectrovalve(electrovalve_id):
    with database.app.app_context():
        electrovalve_dao = DaoFactory().createElectrovalveDAO()
        gpio_dao = DaoFactory().createGPIODAO()
        board = Board()

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)

        logger.info('Soil sensor for electrovalve with id {} has observed humidity {}% \with the humidity threshold {}%'
            .format(electrovalve_id, electrovalve['current_humidity'], electrovalve['humidity_threshold']))

        electrovalve_pin = gpio_dao.getPinByName(electrovalve['electrovalve_pin'])

        if electrovalve['current_humidity'] <= electrovalve['humidity_threshold']:
            electrovalve['watering'] = True
            electrovalve_dao.updateElectrovalveById(electrovalve, electrovalve_id)
            board.initBoard()
            board.setupOutputPin(electrovalve_pin)
            board.enablePin(electrovalve_pin)

            logger.error('watering for ... {} seconds'.format(electrovalve['duration']))
            time.sleep(electrovalve['duration'])

            board.disablePin(electrovalve_pin)
            electrovalve['watering'] = False
            electrovalve['last_water'] = datetime.utcnow()
            electrovalve_dao.updateElectrovalveById(electrovalve, electrovalve_id)
