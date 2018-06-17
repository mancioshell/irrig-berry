import logging
from pytz import utc
import os

from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO, emit

from waterberry.socket.socket import ElectrovalveSocket
from waterberry.db.dao_factory import DaoFactory
from waterberry.jobs.job_factory import JobFactory
from waterberry.scheduler.scheduler import Scheduler
from waterberry.gpio.board import Board
from waterberry.gpio.dht_sensor import DHTSensor
from waterberry.resources.electrovalve import Electrovalve
from waterberry.resources.electrovalve_list import ElectrovalveList
from waterberry.resources.pin_list import PinList
from waterberry.resources.dht_sensor_resource import Sensor
from waterberry.resources.dht_sensor_list_resource import SensorList
from waterberry.utils.json_encoder import CustomJSONEncoder
from waterberry.utils.logger import logger

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

print os.environ['PLATFORM']

app = Flask(__name__, static_url_path='', static_folder='public')
app.json_encoder = CustomJSONEncoder

@app.route('/')
def root():
    return app.send_static_file('index.html')

board = Board()
dao_factory = DaoFactory()

app = dao_factory.initApp(app)
electrovalve_dao = dao_factory.createElectrovalveDAO()
gpio_dao = dao_factory.createGPIODAO()
dht_sensor_dao = dao_factory.createDHTSensorDAO()
dht_sensor_dao.initSensor()

dht_sensor = DHTSensor(dht_sensor_dao, gpio_dao)

scheduler = Scheduler(app)
scheduler = scheduler.getScheduler()
job_factory = JobFactory(scheduler, gpio_dao, board)

job_factory.makeJob('dht_sensor').remove()
job_factory.makeJob('dht_sensor').add()

socketio = SocketIO(app, logger=True,  engineio_logger=True)
socketio.on_namespace(ElectrovalveSocket(socketio, electrovalve_dao, dht_sensor))

api = Api(app)

api.add_resource(Electrovalve, '/api/electrovalves/<string:electrovalve_id>',
    resource_class_kwargs={ 'electrovalve_dao': electrovalve_dao, 'gpio_dao': gpio_dao, 'job_factory': job_factory})
api.add_resource(ElectrovalveList, '/api/electrovalves',
    resource_class_kwargs={ 'electrovalve_dao': electrovalve_dao, 'gpio_dao': gpio_dao, 'job_factory': job_factory})

api.add_resource(PinList, '/api/pins', resource_class_kwargs={ 'gpio_dao': gpio_dao})

api.add_resource(Sensor, '/api/sensor', resource_class_kwargs={ 'dht_sensor_dao': dht_sensor_dao, 'gpio_dao': gpio_dao})
api.add_resource(SensorList, '/api/sensors', resource_class_kwargs={ 'dht_sensor_dao': dht_sensor_dao})

if __name__ == "__main__":
    socketio.run(app, debug=True)
