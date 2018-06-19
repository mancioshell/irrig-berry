from datetime import datetime

from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.manual_electrovalve import ManualElectrovalveExecutor
from waterberry.executors.next_watering import NextWaterExecutor
from waterberry.utils.logger import logger

class ScheduledJob:
    def __init__(self, scheduler, board):
        self.scheduler = scheduler
        self.board = board

    def add(self, electrovalve_id, electrovalve):
        timetable = electrovalve['timetable']
        next_water_job_id = "{}_next_watering".format(electrovalve_id)
        for count, calendar in enumerate(timetable):
            job_id = "{}_{}".format(electrovalve_id, count)
            day_of_week = calendar['day']
            date_time = calendar['time']

            time = datetime.strptime(date_time, '%H:%M')

            self.scheduler.add_job(ManualElectrovalveExecutor, 'cron', day_of_week=day_of_week,
                hour=time.hour, minute=time.minute, args=[electrovalve_id], id=job_id)

        self.scheduler.add_job(NextWaterExecutor, 'interval', minutes=30, args=[electrovalve_id],
            id=next_water_job_id)


    def remove(self, electrovalve_id, electrovalve):
        timetable = electrovalve['timetable']
        self.board.initBoard()
        self.board.cleanupPin(electrovalve['electrovalve_pin'])

        for count, calendar in enumerate(timetable):
            job_id = "{}_{}".format(electrovalve_id, count)
            try:
                self.scheduler.remove_job(job_id)
            except JobLookupError:
                pass

        next_water_job_id = "{}_next_watering".format(electrovalve_id)
        try:
            self.scheduler.remove_job(next_water_job_id)
        except JobLookupError:
            pass

    def reschedule(self, electrovalve_id, electrovalve):
        timetable = electrovalve['timetable']
        for count, calendar in enumerate(timetable):
            job_id = "{}_{}".format(electrovalve_id, count)
            day_of_week = calendar['day']
            date_time = calendar['time']

            time = datetime.strptime(date_time, '%H:%M')

            self.scheduler.reschedule_job(job_id, trigger='cron', day_of_week=day_of_week,
                hour=time.hour, minute=time.minute)
