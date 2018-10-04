from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.utils.logger import logger

class PinList(Resource):
    def __init__(self, **kwargs):
        self.electrovalve_dao = kwargs['electrovalve_dao']
        self.raspberry_dao = kwargs['raspberry_dao']
        self.dht_sensor_dao = kwargs['dht_sensor_dao']

    def get(self):
        """Get all available pins"""
        sensor = self.dht_sensor_dao.getSensor()        
        electrovalves = self.electrovalve_dao.getAllElectrovalves()
        used_pins = []
        for electrovalve in electrovalves:
            used_pins = used_pins + electrovalve.getUsedPins()

        used_pins.append(sensor.pin)

        raspberry = self.raspberry_dao.getRasberry()
        available_pins = list(set(raspberry.getPinList()) - set(used_pins))

        return jsonify(available_pins)
