from datetime import datetime
from apscheduler.jobstores.base import JobLookupError

from waterberry.jobs.manual_electrovalve import ManualElectrovalve
from waterberry.jobs.automatic_electrovalve import AutomaticElectrovalve
from waterberry.jobs.soil_sensor import SoilSensor

from waterberry.utils.logger import logger

def pippo(electrovalve_id):
    pass

class JobFacade:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.automatic_electrovalve = AutomaticElectrovalve
        self.manual_electrovalve = ManualElectrovalve
        self.soil_sensor = SoilSensor

    def addManualJob(self, electrovalve_id):
        """ addManualJob """
        manual_job_id = "{}_manual".format(electrovalve_id)
        self.scheduler.add_job(self.manual_electrovalve, 'date', args=[electrovalve_id],
            id=manual_job_id)
        return

    def rescheduleManualJob(self, electrovalve_id):
        """ rescheduleManualJob """
        manual_job_id = "{}_manual".format(electrovalve_id)
        self.scheduler.reschedule_job(manual_job_id, trigger='date')

    def removeManualJob(self, electrovalve_id):
        """ removeManualJob """
        try:
            self.scheduler.remove_job(electrovalve_id)
        except JobLookupError:
            logger.error("No job with id {} was found".format(electrovalve_id))
            pass
        return

    def addAutomaticJob(self, electrovalve_id):
        """ addAutomaticJob """
        job_id = "{}_soil".format(electrovalve_id)
        self.scheduler.add_job(self.soil_sensor, 'interval', seconds=30,
            args=[electrovalve_id], id=job_id)
        self.scheduler.add_job(self.automatic_electrovalve, 'interval', minutes=1,
            args=[electrovalve_id], id=electrovalve_id)
        return

    def rescheduleAutomaticJob(self, electrovalve_id):
        """ rescheduleAutomaticJob """
        job_id = "{}_soil".format(electrovalve_id)

        self.scheduler.reschedule_job(job_id, trigger='interval', seconds=30)
        self.scheduler.reschedule_job(electrovalve_id, trigger='interval', minutes=1)

    def removeAutomaticJob(self, electrovalve_id):
        """ removeAutomaticJob """
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
        """ addScheduledJob """
        job_id = "{}_{}".format(electrovalve_id, count)
        day_of_week = calendar['day']
        date_time = calendar['time']

        time = datetime.strptime(date_time, '%H:%M')

        self.scheduler.add_job(self.manual_electrovalve, 'cron', day_of_week=day_of_week,
            hour=time.hour, minute=time.minute, args=[electrovalve_id], id=job_id)
        return

    def rescheduleScheduledJob(self, count, calendar, electrovalve_id):
        """ rescheduleScheduledJob """
        job_id = "{}_{}".format(electrovalve_id, count)
        day_of_week = calendar['day']
        date_time = calendar['time']

        time = datetime.strptime(date_time, '%H:%M')

        self.scheduler.reschedule_job(job_id, trigger='cron', day_of_week=day_of_week,
            hour=time.hour, minute=time.minute)

    def removeScheduledJob(self, count, electrovalve_id):
        """ removeScheduledJob """
        job_id = "{}_{}".format(electrovalve_id, count)
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            pass
        return
