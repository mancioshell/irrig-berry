from datetime import datetime

from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.manual_electrovalve import ManualElectrovalveExecutor
from waterberry.executors.next_watering import NextWaterExecutor
from waterberry.utils.logger import logger

class ScheduledJob:
    def __init__(self, scheduler, electrovalve):
        self.scheduler = scheduler        
        self.electrovalve = electrovalve

    def add(self):       
        next_water_job_id = "{}_next_watering".format(self.electrovalve.id)
        for count, calendar in enumerate(self.electrovalve.timetable):
            job_id = "scheduled_{}_{}".format(self.electrovalve.id, count)
            day_of_week = calendar['day']
            date_time = calendar['time']

            time = datetime.strptime(date_time, '%H:%M')

            self.scheduler.add_job(ManualElectrovalveExecutor, 'cron', day_of_week=day_of_week,
                hour=time.hour, minute=time.minute, args=[self.electrovalve.id], id=job_id)

        self.scheduler.add_job(NextWaterExecutor, 'interval', hours=6, args=[self.electrovalve.id],
            id=next_water_job_id)


    def remove(self):
        for count in enumerate(self.electrovalve.timetable):
            job_id = "scheduled_{}_{}".format(self.electrovalve.id, count)
            try:
                self.scheduler.remove_job(job_id)
            except JobLookupError:
                pass

        next_water_job_id = "{}_next_watering".format(self.electrovalve.id)
        try:
            self.scheduler.remove_job(next_water_job_id)
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
