from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.utils.logger import logger

class PinList(Resource):
    def __init__(self, **kwargs):
        self.electrovalve_dao = kwargs['electrovalve_dao']
        self.gpio_dao = kwargs['gpio_dao']

    def get(self):
        """Get all available pins"""
        electrovalves = self.electrovalve_dao.getElectrovalveList()
        available_pins = self.gpio_dao.getAvailablePinList(electrovalves)
        return jsonify(available_pins)
