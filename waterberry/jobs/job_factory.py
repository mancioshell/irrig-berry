from waterberry.jobs.manual_job import ManualJob
from waterberry.jobs.scheduled_job import ScheduledJob
from waterberry.jobs.automatic_job import AutomaticJob
from waterberry.jobs.dht_sensor_job import DHTSensorJob

class JobFactory:
    def __init__(self, scheduler, board, raspberry):
        self.scheduler = scheduler
        self.board = board
        self.raspberry = raspberry

    def makeJob(self, electrovalve):
        switcher = {
            'manual': ManualJob(self.scheduler, self.board, self.raspberry, electrovalve),
            'automatic': AutomaticJob(self.scheduler, self.board, self.raspberry, electrovalve),
            'scheduled': ScheduledJob(self.scheduler, self.board, self.raspberry, electrovalve),
            'dht_sensor': DHTSensorJob(self.scheduler)
        }
        return switcher.get(electrovalve.mode, ManualJob(self.scheduler, self.board, self.raspberry, electrovalve))
