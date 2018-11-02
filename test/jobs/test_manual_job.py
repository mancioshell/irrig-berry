import pytest

from mock import MagicMock, Mock, PropertyMock
import os
import sys
import inspect
sys.modules['waterberry.utils.logger'] = Mock()
os.environ["PLATFORM"] = "local"
from waterberry.jobs.manual_job import ManualJob
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.background import BackgroundScheduler

electrovalve_id = 1

@pytest.fixture(scope="module")
def job():
    scheduler = BackgroundScheduler()
    scheduler.start()

    electrovalve = MagicMock(id=electrovalve_id)
    job = ManualJob(scheduler, electrovalve)

    yield job  # provide the fixture value

    scheduler.shutdown(False)


def test_add_existing_job_without_error(job):
  job.add()
  job.add()
  assert len(job.scheduler.get_jobs()) == 1

def test_add_success(job):  
  manual_job_id = "{}_manual".format(electrovalve_id)
  job.add()
  assert len(job.scheduler.get_jobs()) == 1
  manual_job = job.scheduler.get_job(manual_job_id)

  assert manual_job is not None
  assert inspect.isfunction(manual_job.func)
  assert manual_job.func.__name__ == 'ManualElectrovalveExecutor'
  assert isinstance(manual_job.trigger, DateTrigger)
