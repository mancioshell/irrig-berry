from pytz import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

rome = timezone('Europe/Rome')

class Scheduler:
    def __init__(self, app):
        jobstores = {
            'default': MongoDBJobStore(host=app.config['MONGO_HOST'], port=app.config['MONGO_PORT'])
        }
        executors = {
            'default': ThreadPoolExecutor(20)
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, timezone=rome)
        self.scheduler.start()

    def getScheduler(self):
        return self.scheduler
