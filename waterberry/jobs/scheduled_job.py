from datetime import datetime

from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from waterberry.executors.manual_electrovalve import ManualElectrovalveExecutor
from waterberry.utils.logger import logger


class ScheduledJob:
    def __init__(self, scheduler, electrovalve):
        self.scheduler = scheduler
        self.electrovalve = electrovalve

    def add(self):
        for count, calendar in enumerate(self.electrovalve.timetable):
            job_id = "scheduled_{}_{}".format(self.electrovalve.id, count)
            day_of_week = calendar['day']
            date_time = calendar['time']

            time = datetime.strptime(date_time, '%H:%M')

            try:
                self.scheduler.add_job(ManualElectrovalveExecutor, 'cron', day_of_week=day_of_week,
                                       hour=time.hour, minute=time.minute, args=[self.electrovalve.id], id=job_id)
            except ConflictingIdError:
                logger.error("Job with id {} was already found".format(job_id))
                self.scheduler.reschedule_job(job_id, trigger='cron',
                                              day_of_week=day_of_week, hour=time.hour, minute=time.minute)

    def remove(self):
        for count in enumerate(self.electrovalve.timetable):
            job_id = "scheduled_{}_{}".format(self.electrovalve.id, count)
            try:
                self.scheduler.remove_job(job_id)
            except JobLookupError:
                pass

    def reschedule(self):
        for count, calendar in enumerate(self.electrovalve.timetable):
            job_id = "{}_{}".format(self.electrovalve.id, count)
            day_of_week = calendar['day']
            date_time = calendar['time']

            time = datetime.strptime(date_time, '%H:%M')

            self.scheduler.reschedule_job(job_id, trigger='cron', day_of_week=day_of_week,
                                          hour=time.hour, minute=time.minute)
