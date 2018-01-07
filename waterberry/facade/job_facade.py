from datetime import datetime
from apscheduler.jobstores.base import JobLookupError

from waterberry.jobs.manual_electrovalve import ManualElectrovalve
from waterberry.jobs.automatic_electrovalve import AutomaticElectrovalve
from waterberry.jobs.soil_sensor import SoilSensor

from waterberry.utils.logger import logger

class JobFacade:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.automatic_electrovalve = AutomaticElectrovalve()
        self.manual_electrovalve = ManualElectrovalve()
        self.soil_sensor = SoilSensor()

    def addManualJob(self, electrovalve_id):
        """ """
        manual_job_id = "{}_manual".format(electrovalve_id)
        self.scheduler.add_job(self.manual_electrovalve, 'date', args=[electrovalve_id],
            id=manual_job_id)
        return

    def removeManualJob(self, electrovalve_id):
        """ """
        try:
            self.scheduler.remove_job(electrovalve_id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(electrovalve_id))
            pass
        return

    def addAutomaticJob(self, electrovalve_id):
        """ """
        job_id = "{}_soil".format(electrovalve_id)
        self.scheduler.add_job(self.soil_sensor, 'interval', seconds=30,
            args=[electrovalve_id], id=job_id)
        self.scheduler.add_job(self.automatic_electrovalve, 'interval', minutes=1,
            args=[electrovalve_id], id=electrovalve_id)
        return

    def removeAutomaticJob(self, electrovalve_id):
        """ """
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
        return

    def addScheduledJob(self, count, calendar, electrovalve_id):
        """ """
        job_id = "{}_{}".format(electrovalve_id, count)
        day_of_week = calendar['day']
        date_time = calendar['time']

        time = datetime.strptime(date_time, '%H:%M')

        self.scheduler.add_job(self.manual_electrovalve, 'cron', day_of_week=day_of_week,
            hour=time.hour, minute=time.minute, args=[electrovalve_id], id=job_id)
        return

    def removeScheduledJob(self, count, electrovalve_id):
        """ """
        job_id = "{}_{}".format(electrovalve_id, count)
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            pass
        return
