from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.automatic_electrovalve import AutomaticElectrovalveExecutor
from waterberry.executors.soil_sensor import SoilSensorExecutor
from waterberry.utils.logger import logger

class AutomaticJob:
    def __init__(self, scheduler, board, raspberry, electrovalve):
        self.scheduler = scheduler
        self.board = board
        self.raspberry = raspberry
        self.electrovalve = electrovalve

    def add(self):
        job_id = "{}_automatic".format(self.electrovalve.id)
        job_id_soil = "{}_soil".format(self.electrovalve.id)

        self.scheduler.add_job(AutomaticElectrovalveExecutor, 'interval', minutes=15,
            args=[self.electrovalve.id], id=job_id)
        self.scheduler.add_job(SoilSensorExecutor, 'interval', minutes=5,
            args=[self.electrovalve.id], id=job_id_soil)

    def remove(self):
        self.board.initBoard()

        pins = self.raspberry.getPinByName(self.electrovalve.getUsedPins())
        self.board.cleanupPin(pins)

        job_id = "{}_automatic".format(self.electrovalve.id)
        job_id_soil = "{}_soil".format(self.electrovalve.id)

        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(self.electrovalve.id))
            pass

        try:
            self.scheduler.remove_job(job_id_soil)
        except JobLookupError:
            logger.error("No job with id {} was found".format(self.electrovalve.id))
            pass

    def reschedule(self):
        self.scheduler.reschedule_job(self.electrovalve.id, trigger='interval', minutes=5)
        job_id = "{}_soil".format(self.electrovalve.id)
        self.scheduler.reschedule_job(job_id, trigger='interval', minutes=1)
