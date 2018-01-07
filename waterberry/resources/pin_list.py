from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.facade.pin_facade import PinFacade
from waterberry.utils.logger import logger

class PinList(Resource):
    def __init__(self, **kwargs):
        self.mongo = kwargs['mongo']
        self.pin_facade = PinFacade(kwargs['mongo'])

    def get(self):
        """Get all pins"""
        logger.info('Get all pins')
        available_pins = self.pin_facade.getAvailablePin()
        return jsonify(available_pins)
