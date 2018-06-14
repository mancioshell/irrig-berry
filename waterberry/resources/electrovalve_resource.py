from flask_restful import Resource
from flask import jsonify, make_response

from waterberry.utils.messages import *
from waterberry.utils.logger import logger

class Forbidden(Exception):
    pass

class ElectrovalveResource(Resource):
    def __init__(self, **kwargs):
        self.electrovalve_dao = kwargs['electrovalve_dao']
        self.gpio_dao = kwargs['gpio_dao']
        self.job_factory = kwargs['job_factory']

    def validatePin(self, electrovalve, data=None):

        available_pins = self.gpio_dao.getAvailablePinList()
        current_electovalve_pin = None
        current_sensor_pin = None
        if data is not None:
            current_sensor_pin = data['sensor_pin'] if 'sensor_pin' in data else None
            current_electovalve_pin = data['electrovalve_pin'] if 'electrovalve_pin' in data else None       

        logger.error('available_pins : {}'.format(available_pins))

        electrovalve_pin = electrovalve['electrovalve_pin']
        sensor_pin = electrovalve['sensor_pin'] if 'sensor_pin' in electrovalve else None

        logger.error('electrovalve_pin : {}'.format(electrovalve_pin))
        logger.error('sensor_pin : {}'.format(sensor_pin))

        if sensor_pin is not None and sensor_pin == electrovalve_pin:
            message = ELECTROVALVE_PIN_ALREADY_IN_USE.format(electrovalve_pin)
            raise Forbidden(jsonify({'message': message}))

        if electrovalve_pin not in available_pins + [current_electovalve_pin, current_sensor_pin]:
            logger.error('electrovalve_pin already in use ...')
            message = ELECTROVALVE_PIN_ALREADY_IN_USE.format(electrovalve_pin)
            raise Forbidden(jsonify({'message': message}))

        if sensor_pin is not None and sensor_pin not in available_pins + [current_electovalve_pin, current_sensor_pin]:
            logger.error('sensor_pin already in use ...')
            message = SENSOR_PIN_ALREADY_IN_USE.format(sensor_pin)
            raise Forbidden(jsonify({'message': message}))

    def isWatering(self, electrovalve):
        if electrovalve['watering']:
            message = ELECTROVALVE_IS_WATERING
            raise Forbidden(jsonify({'message': message}))
