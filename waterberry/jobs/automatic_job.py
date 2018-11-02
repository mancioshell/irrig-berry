from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from waterberry.executors.automatic_electrovalve import AutomaticElectrovalveExecutor
from waterberry.executors.soil_sensor import SoilSensorExecutor
from waterberry.utils.logger import logger

class AutomaticJob:
    JOB_INTERVAL = 15
    JOB_SOIL_INTERVAL = 5

    def __init__(self, scheduler, electrovalve):        
        self.scheduler = scheduler
        self.electrovalve = electrovalve

    def add(self):
        job_id = "{}_automatic".format(self.electrovalve.id)
        job_id_soil = "{}_soil".format(self.electrovalve.id)

        try:
            self.scheduler.add_job(AutomaticElectrovalveExecutor, 'interval', minutes=self.JOB_INTERVAL,
                args=[self.electrovalve.id], id=job_id)
        except ConflictingIdError:
            logger.error("Job with id {} was already found".format(job_id))
            self.scheduler.reschedule_job(job_id, trigger='interval', minutes=self.JOB_INTERVAL)

        try:
            self.scheduler.add_job(SoilSensorExecutor, 'interval', minutes=self.JOB_SOIL_INTERVAL, 
                args=[self.electrovalve.id], id=job_id_soil)
        except ConflictingIdError:
            logger.error("Job with id {} was already found".format(job_id_soil))
            self.scheduler.reschedule_job(job_id_soil, trigger='interval', minutes=self.JOB_SOIL_INTERVAL)     

    def remove(self):
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
        job_id = "{}_automatic".format(self.electrovalve.id)
        self.scheduler.reschedule_job(job_id, trigger='interval', minutes=self.JOB_INTERVAL)
        job_id_soil = "{}_soil".format(self.electrovalve.id)
        self.scheduler.reschedule_job(job_id_soil, trigger='interval', minutes=self.JOB_SOIL_INTERVAL)