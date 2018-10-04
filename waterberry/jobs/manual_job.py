from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.manual_electrovalve import ManualElectrovalveExecutor
from waterberry.utils.logger import logger

class ManualJob:
    def __init__(self, scheduler, board, raspberry, electrovalve):
        self.scheduler = scheduler
        self.board = board
        self.raspberry = raspberry
        self.electrovalve = electrovalve

    def add(self):
        manual_job_id = "{}_manual".format(self.electrovalve.id)
        self.scheduler.add_job(ManualElectrovalveExecutor, 'date', args=[self.electrovalve.id], id=manual_job_id)

    def remove(self):
        self.board.initBoard()
        pin = self.raspberry.getPinByName(self.electrovalve.getUsedPins())
        self.board.cleanupPin(pin)
        try:
            self.scheduler.remove_job(self.electrovalve.id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(self.electrovalve.id))
            pass

    def reschedule(self):
        manual_job_id = "{}_manual".format(self.electrovalve.id)
        self.scheduler.reschedule_job(manual_job_id, trigger='date')
