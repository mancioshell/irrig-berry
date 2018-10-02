import logging
from pytz import utc
import os

from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO, emit

from waterberry.socket.socket import ElectrovalveSocket
from waterberry.db.dao_factory import DaoFactory
from waterberry.jobs.job_factory import JobFactory
from jobs.scheduler.scheduler import Scheduler
from waterberry.ecomponents.board import Board
from waterberry.ecomponents.dht_sensor import DHTSensor
from waterberry.resources.electrovalve import Electrovalve
from waterberry.resources.electrovalve_list import ElectrovalveList
from waterberry.resources.pin_list import PinList
from waterberry.resources.dht_sensor_resource import Sensor
from waterberry.resources.raspberry import Raspberry
from waterberry.utils.json_encoder import CustomJSONEncoder
from waterberry.utils.logger import logger

from waterberry.utils.definition import ROOT_DIR

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

print ROOT_DIR
print os.environ['PLATFORM']

app = Flask(__name__, static_url_path='', static_folder='public')
app.json_encoder = CustomJSONEncoder

@app.route('/')
def root():
    return app.send_static_file('index.html')

dao_factory = DaoFactory()

app = dao_factory.initApp(app)
electrovalve_dao = dao_factory.createElectrovalveDAO()
raspberry_dao = dao_factory.createRaspberryDAO()
raspberry_dao.initGPIO()
dht_sensor_dao = dao_factory.createDHTSensorDAO()
dht_sensor_dao.initSensor()

dht_sensor = DHTSensor(dht_sensor_dao, raspberry_dao)
board = Board(raspberry_dao)

scheduler = Scheduler(app)
scheduler = scheduler.getScheduler()
job_factory = JobFactory(scheduler, board)

job_factory.makeJob('dht_sensor').remove()
job_factory.makeJob('dht_sensor').add()

socketio = SocketIO(app, logger=True,  engineio_logger=True)
socketio.on_namespace(ElectrovalveSocket(socketio, electrovalve_dao, dht_sensor))

api = Api(app)

api.add_resource(Electrovalve, '/api/electrovalves/<string:electrovalve_id>',
    resource_class_kwargs={ 'electrovalve_dao': electrovalve_dao, 'raspberry_dao': raspberry_dao, 'job_factory': job_factory, 'dht_sensor_dao': dht_sensor_dao})
api.add_resource(ElectrovalveList, '/api/electrovalves',
    resource_class_kwargs={ 'electrovalve_dao': electrovalve_dao, 'raspberry_dao': raspberry_dao, 'job_factory': job_factory, 'dht_sensor_dao': dht_sensor_dao})

api.add_resource(PinList, '/api/pins', resource_class_kwargs={ 'dht_sensor_dao': dht_sensor_dao, 'raspberry_dao': raspberry_dao, 'electrovalve_dao': electrovalve_dao})

api.add_resource(Sensor, '/api/sensors', resource_class_kwargs={ 'dht_sensor_dao': dht_sensor_dao, 'raspberry_dao': raspberry_dao, 'electrovalve_dao': electrovalve_dao})

api.add_resource(Raspberry, '/api/raspberry', resource_class_kwargs={ 'raspberry_dao': raspberry_dao})

if __name__ == "__main__":
    socketio.run(app, debug=True)
