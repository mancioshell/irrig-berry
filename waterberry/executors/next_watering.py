import time
from datetime import datetime

from waterberry.scheduler.scheduler import Scheduler
from waterberry.db.dao_factory import database, DaoFactory
from waterberry.utils.logger import logger

def NextWaterExecutor(electrovalve_id):
    with database.app.app_context():
        electrovalve_dao = DaoFactory().createElectrovalveDAO()

        scheduler = Scheduler(database.app)
        scheduler = scheduler.getScheduler()

        filter_job_by_id = lambda job: job.id.split("_")[0] == 'scheduled' and job.id.split("_")[1] == electrovalve_id
        next_run_time_job = lambda job1, job2: job1 if job1.next_run_time <= job2.next_run_time else job2

        jobs = scheduler.get_jobs()
        selected_jobs = filter(filter_job_by_id, jobs)
        next_job = reduce(next_run_time_job, selected_jobs)

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)
        if next_job is not None: electrovalve['next_water'] = next_job.next_run_time
        electrovalve_dao.updateElectrovalveById(electrovalve, electrovalve_id)
