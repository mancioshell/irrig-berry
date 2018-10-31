from waterberry.jobs.manual_job import ManualJob
from waterberry.jobs.scheduled_job import ScheduledJob
from waterberry.jobs.automatic_job import AutomaticJob
from waterberry.jobs.dht_sensor_job import DHTSensorJob

class JobFactory:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def makeJob(self, electrovalve):        
        mode = electrovalve.mode if type(electrovalve) is object else electrovalve
        switcher = {
            'manual': ManualJob(self.scheduler, electrovalve),
            'automatic': AutomaticJob(self.scheduler, electrovalve),
            'scheduled': ScheduledJob(self.scheduler, electrovalve),
            'dht_sensor': DHTSensorJob(self.scheduler)
        }
        return switcher.get(mode, ManualJob(self.scheduler, electrovalve))
