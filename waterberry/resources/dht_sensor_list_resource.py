from flask_restful import Resource
from flask import request, jsonify, make_response
from waterberry.utils.logger import logger

class SensorList(Resource):
    def __init__(self, **kwargs):
        self.dht_sensor_dao = kwargs['dht_sensor_dao']

    def get(self):
        sensor_type_list = self.dht_sensor_dao.getSensorTypeList()
        return jsonify(sensor_type_list)
