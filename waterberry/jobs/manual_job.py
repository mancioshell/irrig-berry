from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.manual_electrovalve import ManualElectrovalveExecutor
from waterberry.utils.logger import logger

class ManualJob:
    def __init__(self, scheduler, board):
        self.scheduler = scheduler
        self.board = board

    def add(self, electrovalve_id, electrovalve=None):
        manual_job_id = "{}_manual".format(electrovalve_id)
        self.scheduler.add_job(ManualElectrovalveExecutor, 'date', args=[electrovalve_id], id=manual_job_id)

    def remove(self, electrovalve_id, electrovalve):
        self.board.initBoard()
        self.board.cleanupPin(electrovalve['electrovalve_pin'])
        try:
            self.scheduler.remove_job(electrovalve_id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(electrovalve_id))
            pass

    def reschedule(self, electrovalve_id, electrovalve=None):
        manual_job_id = "{}_manual".format(electrovalve_id)
        self.scheduler.reschedule_job(manual_job_id, trigger='date')
