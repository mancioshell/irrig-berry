from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.utils.validator import RaspberrySchema
from waterberry.utils.logger import logger

class Raspberry(Resource):
    def __init__(self, **kwargs):
        self.raspberry_dao = kwargs['raspberry_dao']

    def get(self):
        """Get all available raspberry pi models"""
        raspberry_models = self.raspberry_dao.getRaspberryModelList()
        return jsonify(raspberry_models)

    def put(self):
        """Set raspberry pi model"""
        json = request.get_json()
        raspberry, errors = RaspberrySchema().load(json)
        if errors:
            return make_response(jsonify({'message': errors}), 400)
        self.raspberry_dao.setRaspberryPiModel(raspberry['model'])
        return make_response(jsonify({}), 201)
