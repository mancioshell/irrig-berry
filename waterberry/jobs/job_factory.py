from waterberry.jobs.manual_job import ManualJob
from waterberry.jobs.scheduled_job import ScheduledJob
from waterberry.jobs.automatic_job import AutomaticJob
from waterberry.jobs.dht_sensor_job import DHTSensorJob

class JobFactory:
    def __init__(self, scheduler, gpio_dao, board):
        self.scheduler = scheduler
        self.gpio_dao = gpio_dao
        self.board = board

    def makeJob(self, mode):
        switcher = {
            'manual': ManualJob(self.scheduler, self.gpio_dao, self.board),
            'automatic': AutomaticJob(self.scheduler, self.gpio_dao, self.board),
            'scheduled': ScheduledJob(self.scheduler, self.gpio_dao, self.board),
            'dht_sensor': DHTSensorJob(self.scheduler)
        }
        return switcher.get(mode, ManualJob(self.scheduler, self.gpio_dao, self.board))
