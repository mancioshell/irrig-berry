from flask_restful import Resource
from flask import request, jsonify, make_response
from waterberry.utils.validator import DHTSensorSchema
from waterberry.utils.messages import *
from waterberry.utils.logger import logger

class Sensor(Resource):
    def __init__(self, **kwargs):
        self.electrovalve_dao = kwargs['electrovalve_dao']
        self.dht_sensor_dao = kwargs['dht_sensor_dao']
        self.raspberry_dao = kwargs['raspberry_dao']

    def get(self):
        sensor = self.dht_sensor_dao.getSensor()
        return jsonify(sensor)

    def put(self):
        json = request.get_json()
        dht_sensor, errors = DHTSensorSchema().load(json)
        if errors:
           return make_response(jsonify({'message': errors}), 400)

        dht_sensor_pin = self.dht_sensor_dao.getSensor()['pin']

        electrovalves = self.electrovalve_dao.getElectrovalveList()
        available_pins = self.raspberry_dao.getAvailablePinList(electrovalves, dht_sensor_pin)

        if dht_sensor['pin'] != dht_sensor_pin and dht_sensor['pin'] not in available_pins:
            logger.error('dht sensor pin already in use ...')
            message = ELECTROVALVE_PIN_ALREADY_IN_USE.format(dht_sensor['pin'])
            return make_response(jsonify({'message': message}), 403)

        self.dht_sensor_dao.setSensorType(dht_sensor['type'])
        self.dht_sensor_dao.setSensorPin(dht_sensor['pin'])

        return make_response(jsonify({}), 201)
