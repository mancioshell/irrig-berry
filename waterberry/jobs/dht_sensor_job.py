from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from waterberry.executors.dht_sensor import DHTSensorExecutor
from waterberry.utils.logger import logger


class DHTSensorJob:
    JOB_INTERVAL = 1

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def add(self):
        try:
            self.scheduler.add_job(DHTSensorExecutor, 'interval',
                                   minutes=self.JOB_INTERVAL, id='dht_sensor')
        except ConflictingIdError:
            logger.error(
                "Job with id {} was already found".format('dht_sensor'))
            self.scheduler.reschedule_job('dht_sensor', trigger='interval',
                                          minutes=self.JOB_INTERVAL)

    def remove(self):
        try:
            self.scheduler.remove_job('dht_sensor')
        except JobLookupError:
            logger.error("No job with id dht_sensor was found")
            pass
