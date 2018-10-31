from mock import MagicMock, Mock, PropertyMock
import os
import sys
import inspect
from datetime import timedelta
sys.modules['waterberry.utils.logger'] = Mock()
os.environ["PLATFORM"] = "local"

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from waterberry.jobs.automatic_job import AutomaticJob

scheduler = BackgroundScheduler()
scheduler.start()

electrovalve_id = 1

electrovalve = MagicMock(id=electrovalve_id)
job = AutomaticJob(scheduler, electrovalve)

def test_add_existing_job_without_error():
    job_id = "{}_automatic".format(electrovalve_id)
    job_id_soil = "{}_soil".format(electrovalve_id)
    job.add()
    job.add()    
           
def test_add_success():
    job_id = "{}_automatic".format(electrovalve_id)
    job_id_soil = "{}_soil".format(electrovalve_id)
    job.add()
    assert len(job.scheduler.get_jobs()) == 2 
    automatic_job = job.scheduler.get_job(job_id)
    soil_job = job.scheduler.get_job(job_id_soil)

    assert automatic_job is not None
    assert soil_job is not None

    assert inspect.isfunction(automatic_job.func)
    assert automatic_job.func.__name__ == 'AutomaticElectrovalveExecutor'    
    assert isinstance(automatic_job.trigger, IntervalTrigger)
    assert automatic_job.trigger.interval  == timedelta(minutes=job.JOB_INTERVAL)

    assert inspect.isfunction(soil_job.func)
    assert soil_job.func.__name__ == 'SoilSensorExecutor'    
    assert isinstance(soil_job.trigger, IntervalTrigger)
    assert soil_job.trigger.interval  == timedelta(minutes=job.JOB_SOIL_INTERVAL)
