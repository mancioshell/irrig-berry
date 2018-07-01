from apscheduler.jobstores.base import JobLookupError
from waterberry.executors.dht_sensor import DHTSensorExecutor
from waterberry.utils.logger import logger

class DHTSensorJob:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def add(self):
        self.scheduler.add_job(DHTSensorExecutor, 'interval', minutes=1, id='dht_sensor')

    def remove(self):
        try:
            self.scheduler.remove_job('dht_sensor')
        except JobLookupError:
            logger.error("No job with id dht_sensor was found")
            pass
