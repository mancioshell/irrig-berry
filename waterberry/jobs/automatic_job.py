from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.automatic_electrovalve import AutomaticElectrovalve
from waterberry.executors.soil_sensor import SoilSensor
from waterberry.utils.logger import logger

class AutomaticJob:
    def __init__(self, scheduler, gpio_dao, board):
        self.scheduler = scheduler
        self.gpio_dao = gpio_dao
        self.board = board

    def add(self, electrovalve_id, electrovalve=None):
        job_id = "{}_soil".format(electrovalve_id)
        self.scheduler.add_job(SoilSensor, 'interval', seconds=30,
            args=[electrovalve_id], id=job_id)
        self.scheduler.add_job(AutomaticElectrovalve, 'interval', minutes=1,
            args=[electrovalve_id], id=electrovalve_id)

    def remove(self, electrovalve_id, electrovalve):
        self.board.initBoard()
        self.board.cleanupPin(self.gpio_dao.getPinByName(electrovalve['electrovalve_pin']))
        self.board.cleanupPin(self.gpio_dao.getPinByName(electrovalve['sensor_pin']))
        job_id = "{}_soil".format(electrovalve_id)
        try:
            self.scheduler.remove_job(electrovalve_id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(electrovalve_id))
            pass
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(electrovalve_id))
            pass

    def reschedule(self, electrovalve_id, electrovalve=None):
        job_id = "{}_soil".format(electrovalve_id)
        self.scheduler.reschedule_job(job_id, trigger='interval', seconds=30)
        self.scheduler.reschedule_job(electrovalve_id, trigger='interval', minutes=1)
