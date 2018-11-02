import pytest
from mock import MagicMock, Mock, PropertyMock
import os
import sys
import inspect
from datetime import timedelta
sys.modules['waterberry.utils.logger'] = Mock()
os.environ["PLATFORM"] = "local"

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from waterberry.jobs.dht_sensor_job import DHTSensorJob

@pytest.fixture(scope="module")
def job():
  scheduler = BackgroundScheduler()
  scheduler.start()

  job = DHTSensorJob(scheduler)

  yield job  # provide the fixture value

  scheduler.shutdown(False)

def test_add_existing_job_without_error(job):
  job.add()
  job.add()
  assert len(job.scheduler.get_jobs()) == 1    
           
def test_add_success(job):   
  job.add()
  assert len(job.scheduler.get_jobs()) == 1
  dht_sensor_job = job.scheduler.get_job('dht_sensor')

  assert dht_sensor_job is not None

  assert inspect.isfunction(dht_sensor_job.func)
  assert dht_sensor_job.func.__name__ == 'DHTSensorExecutor'    
  assert isinstance(dht_sensor_job.trigger, IntervalTrigger)
  assert dht_sensor_job.trigger.interval  == timedelta(minutes=job.JOB_INTERVAL)
