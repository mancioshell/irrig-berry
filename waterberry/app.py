import logging
from pytz import utc

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
from waterberry.utils.json_encoder import CustomJSONEncoder
from waterberry.utils.logger import logger

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

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

sensor_data = dht_sensor_dao.getSensorData()
dht_sensor = DHTSensor(sensor_data['type'], sensor_data['pin'])

scheduler = Scheduler(app)
scheduler = scheduler.getScheduler()
job_factory = JobFactory(scheduler, gpio_dao, board)

socketio = SocketIO(app, logger=True,  engineio_logger=True)
socketio.on_namespace(ElectrovalveSocket(socketio, electrovalve_dao, dht_sensor))

api = Api(app)

api.add_resource(Electrovalve, '/api/electrovalves/<string:electrovalve_id>',
    resource_class_kwargs={ 'electrovalve_dao': electrovalve_dao, 'gpio_dao': gpio_dao, 'job_factory': job_factory})
api.add_resource(ElectrovalveList, '/api/electrovalves',
    resource_class_kwargs={ 'electrovalve_dao': electrovalve_dao, 'gpio_dao': gpio_dao, 'job_factory': job_factory})
api.add_resource(PinList, '/api/pins', resource_class_kwargs={ 'gpio_dao': gpio_dao})

if __name__ == "__main__":
    socketio.run(app, debug=True)
