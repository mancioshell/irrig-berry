from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from waterberry.executors.manual_electrovalve import ManualElectrovalveExecutor
from waterberry.utils.logger import logger

class ManualJob:
    def __init__(self, scheduler, electrovalve):
        self.scheduler = scheduler       
        self.electrovalve = electrovalve

    def add(self):
        manual_job_id = "{}_manual".format(self.electrovalve.id)
        try:
            self.scheduler.add_job(ManualElectrovalveExecutor, 'date', args=[self.electrovalve.id], id=manual_job_id)
        except ConflictingIdError:
            logger.error("Job with id {} was already found".format(manual_job_id))
            self.scheduler.reschedule_job(manual_job_id, trigger='date')       

    def remove(self):        
        try:
            self.scheduler.remove_job(self.electrovalve.id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(self.electrovalve.id))
            pass

    def reschedule(self):
        manual_job_id = "{}_manual".format(self.electrovalve.id)
        self.scheduler.reschedule_job(manual_job_id, trigger='date')
