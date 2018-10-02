from waterberry.jobs.manual_job import ManualJob
from waterberry.jobs.scheduled_job import ScheduledJob
from waterberry.jobs.automatic_job import AutomaticJob
from waterberry.jobs.dht_sensor_job import DHTSensorJob

class JobFactory:
    def __init__(self, scheduler, board, raspberry):
        self.scheduler = scheduler
        self.board = board
        self.raspberry = raspberry

    def makeJob(self, mode):
        switcher = {
            'manual': ManualJob(self.scheduler, self.board, self.raspberry),
            'automatic': AutomaticJob(self.scheduler, self.board, self.raspberry),
            'scheduled': ScheduledJob(self.scheduler, self.board, self.raspberry),
            'dht_sensor': DHTSensorJob(self.scheduler)
        }
        return switcher.get(mode, ManualJob(self.scheduler, self.board, self.raspberry))
