from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.resources.electrovalve_resource import ElectrovalveResource
from waterberry.utils.validator import ElectrovalveSchema
from waterberry.utils.messages import ELECTROVALVE_PIN_ALREADY_IN_USE, SENSOR_PIN_ALREADY_IN_USE
from waterberry.utils.logger import logger

class ElectrovalveList(ElectrovalveResource):
    def __init__(self, **kwargs):
        self.mongo = kwargs['mongo']
        super(ElectrovalveList, self).__init__(**kwargs)

    def get(self):
        """Get all electrovalves"""
        logger.info('Get all electrovalves')
        electrovalves = self.mongo.db.electrovalve.find()
        return jsonify(list(electrovalves))

    def delete(self):
        """Delete all electrovalves"""
        logger.info('Delete all electrovalves')
        electrovalves = self.mongo.db.electrovalve.find()
        for electrovalve in electrovalves:
            self.removeJob(electrovalve, electrovalve['_id'])
        electrovalves = self.mongo.db.electrovalve.remove()
        return jsonify([])

    def post(self):
        """Create new electrovalve"""
        json = request.get_json()
        electrovalve, errors = ElectrovalveSchema().load(json)
        logger.info(electrovalve)
        if errors:
            return make_response(jsonify({'message': errors}), 400)

        self.validatePin(electrovalve)

        electrovalve['watering'] = False

        result = self.mongo.db.electrovalve.insert_one(electrovalve)
        electrovalve_id = str(result.inserted_id)
        self.addJob(electrovalve, electrovalve_id)

        return jsonify({'id': electrovalve_id})
