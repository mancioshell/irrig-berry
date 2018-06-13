from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.utils.logger import logger

class PinList(Resource):
    def __init__(self, **kwargs):
        self.gpio_dao = kwargs['gpio_dao']

    def get(self):
        """Get all available pins"""
        available_pins = self.gpio_dao.getAvailablePinList()
        return jsonify(available_pins)
