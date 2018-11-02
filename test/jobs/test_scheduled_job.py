import pytest
from mock import MagicMock, Mock, PropertyMock
import os
import sys
import inspect
sys.modules['waterberry.utils.logger'] = Mock()
os.environ["PLATFORM"] = "local"

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from waterberry.jobs.scheduled_job import ScheduledJob

electrovalve_id = 1
timetable = [{'day': 'mon', 'time': '13:30'}, {'day': 'thu', 'time': '8:30'}]
job_ids = []
for count, _ in enumerate(timetable):
  job_id = "scheduled_{}_{}".format(electrovalve_id, count)
  job_ids.append(job_id)

@pytest.fixture(scope="module")
def job():
  scheduler = BackgroundScheduler()
  scheduler.start() 

  electrovalve = MagicMock(id=electrovalve_id, timetable=timetable)
  job = ScheduledJob(scheduler, electrovalve)

  yield job  # provide the fixture value

  scheduler.shutdown(False)

def test_add_existing_job_without_error(job):
    job.add()
    job.add()
    assert len(job.scheduler.get_jobs()) == len(job_ids)

def test_add_success(job):
    job.add()
    assert len(job.scheduler.get_jobs()) == len(job_ids)

    for job_id in job_ids:
      scheduled_job = job.scheduler.get_job(job_id)
      assert scheduled_job is not None
      assert inspect.isfunction(scheduled_job.func)
      assert scheduled_job.func.__name__ == 'ManualElectrovalveExecutor'
      assert isinstance(scheduled_job.trigger, CronTrigger)

    
