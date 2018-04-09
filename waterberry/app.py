import logging
from pytz import utc

from flask import Flask
from flask_restful import Api
from db.pymongo import mongo

from flask_socketio import SocketIO, emit
from socket.socket import ElectrovalveSocket

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from waterberry.facade.gpio_facade import GPIOFacade
from waterberry.resources.electrovalve import Electrovalve
from waterberry.resources.electrovalve_list import ElectrovalveList
from waterberry.resources.pin_list import PinList
from waterberry.utils.json_encoder import CustomJSONEncoder
from waterberry.utils.logger import logger

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'waterberry_db'
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__, static_url_path='', static_folder='public')
app.json_encoder = CustomJSONEncoder

@app.route('/')
def root():
    return app.send_static_file('index.html')

app.config['MONGO_HOST'] = MONGO_HOST
app.config['MONGO_PORT'] = MONGO_PORT
app.config["MONGO_DBNAME"] = MONGO_DBNAME

mongo.init_app(app, config_prefix='MONGO')
mongo.app = app
socketio = SocketIO(app, logger=True,  engineio_logger=True)
socketio.on_namespace(ElectrovalveSocket(socketio))

jobstores = {
    'default': MongoDBJobStore(host=MONGO_HOST, port=MONGO_PORT)
}
executors = {
    'default': ThreadPoolExecutor(20)
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
scheduler.start()

api = Api(app)

api.add_resource(Electrovalve, '/api/electrovalves/<string:electrovalve_id>',
    resource_class_kwargs={ 'mongo': mongo, 'scheduler': scheduler})
api.add_resource(ElectrovalveList, '/api/electrovalves',
    resource_class_kwargs={ 'mongo': mongo, 'scheduler': scheduler})
api.add_resource(PinList, '/api/pins', resource_class_kwargs={ 'mongo': mongo})

if __name__ == "__main__":
    socketio.run(app, debug=True)
