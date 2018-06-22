from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.utils.logger import logger

class PinList(Resource):
    def __init__(self, **kwargs):
        self.electrovalve_dao = kwargs['electrovalve_dao']
        self.gpio_dao = kwargs['gpio_dao']
        self.dht_sensor_dao = kwargs['dht_sensor_dao']

    def get(self):
        """Get all available pins"""
        dht_sensor_pin = self.dht_sensor_dao.getSensor()['pin']
        electrovalves = self.electrovalve_dao.getElectrovalveList()
        available_pins = self.gpio_dao.getAvailablePinList(electrovalves, dht_sensor_pin)
        return jsonify(available_pins)
