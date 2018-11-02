import time
from datetime import datetime

from waterberry.jobs.scheduler import Scheduler
from waterberry.db.dao_factory import database, DaoFactory
from waterberry.models.electrovalve import ScheduledElectrovalve
from waterberry.ecomponents.board import Board
from waterberry.utils.logger import logger

def filter_job_by_id(job, electrovalve):
    return job.id.split("_")[0] == 'scheduled' and job.id.split("_")[1] == electrovalve.id

def next_run_time_job(job1, job2):
    return job1 if job1.next_run_time <= job2.next_run_time else job2

def next_watering(electrovalve):
    scheduler = Scheduler(database.app)
    scheduler = scheduler.getScheduler()

    jobs = scheduler.get_jobs()
    selected_jobs = filter(
        lambda job: filter_job_by_id(job, electrovalve), jobs)
    next_job = reduce(next_run_time_job, selected_jobs)
    return next_job.next_run_time

def ManualElectrovalveExecutor(electrovalve_id):
    with database.app.app_context():
        electrovalve_dao = DaoFactory().createElectrovalveDAO()
        raspberry_dao = DaoFactory().createRaspberryDAO()
        board = Board()
        raspberry = raspberry_dao.getRasberry()

        electrovalve = electrovalve_dao.getElectrovalveById(electrovalve_id)

        logger.info('ManualElectrovalveExecutor job started ...')
        logger.info('Water electrovalve with id {} at pin {}'.format(
            electrovalve_id, electrovalve.getUsedPins()))

        electrovalve.watering = True
        electrovalve_dao.updateElectrovalveById(electrovalve)
        pin = raspberry.getPinByName(electrovalve.getUsedPins())

        board.initBoard()
        board.setupOutputPin(pin)
        board.enablePin(pin)

        logger.info('watering for ... {} seconds'.format(
            electrovalve['duration']))
        time.sleep(electrovalve['duration'])

        board.disablePin(pin)

        if isinstance(electrovalve, ScheduledElectrovalve):
            electrovalve.next_water = next_watering(electrovalve)
        electrovalve.watering = False
        electrovalve.last_water = datetime.utcnow()
        electrovalve_dao.updateElectrovalveById(electrovalve)
