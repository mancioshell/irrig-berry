from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.automatic_electrovalve import AutomaticElectrovalveExecutor
from waterberry.executors.soil_sensor import SoilSensorExecutor
from waterberry.utils.logger import logger

class AutomaticJob:
    def __init__(self, scheduler, board, raspberry):
        self.scheduler = scheduler
        self.board = board
        self.raspberry = raspberry

    def add(self, electrovalve_id, electrovalve=None):
        job_id = "{}_automatic".format(electrovalve_id)
        job_id_soil = "{}_soil".format(electrovalve_id)

        self.scheduler.add_job(AutomaticElectrovalveExecutor, 'interval', minutes=15,
            args=[electrovalve_id], id=job_id)
        self.scheduler.add_job(SoilSensorExecutor, 'interval', minutes=5,
            args=[electrovalve_id], id=job_id_soil)

    def remove(self, electrovalve_id, electrovalve):
        self.board.initBoard()

        electrovalve_pin = self.raspberry.getPinByName(electrovalve['electrovalve_pin'])
        pin_di = self.raspberry.getPinByName(electrovalve['pin_di'])
        pin_do = self.raspberry.getPinByName(electrovalve['pin_do'])
        pin_clk = self.raspberry.getPinByName(electrovalve['pin_clk'])
        pin_cs = self.raspberry.getPinByName(electrovalve['pin_cs'])

        self.board.cleanupPin([electrovalve_pin, pin_di, pin_do, pin_clk, pin_cs])

        job_id = "{}_automatic".format(electrovalve_id)
        job_id_soil = "{}_soil".format(electrovalve_id)

        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(electrovalve_id))
            pass

        try:
            self.scheduler.remove_job(job_id_soil)
        except JobLookupError:
            logger.error("No job with id {} was found".format(electrovalve_id))
            pass

    def reschedule(self, electrovalve_id, electrovalve=None):
        self.scheduler.reschedule_job(electrovalve_id, trigger='interval', minutes=5)
        job_id = "{}_soil".format(electrovalve_id)
        self.scheduler.reschedule_job(job_id, trigger='interval', minutes=1)
