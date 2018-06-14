from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.resources.electrovalve_resource import ElectrovalveResource, Forbidden
from waterberry.utils.validator import ElectrovalveSchema
from waterberry.utils.messages import ELECTROVALVE_PIN_ALREADY_IN_USE, SENSOR_PIN_ALREADY_IN_USE
from waterberry.utils.logger import logger

class ElectrovalveList(ElectrovalveResource):
    def __init__(self, **kwargs):
        super(ElectrovalveList, self).__init__(**kwargs)

    def get(self):
        """Get all electrovalves"""
        electrovalves = self.electrovalve_dao.getElectrovalveList()
        return jsonify(list(electrovalves))

    def delete(self):
        """Delete all electrovalves"""
        electrovalves = self.electrovalve_dao.getElectrovalveList()
        for electrovalve in electrovalves:
            self.job_factory.makeJob(electrovalve['mode']).remove(electrovalve['_id'], electrovalve)

        electrovalves = self.electrovalve_dao.deleteElectrovalveList()
        return jsonify([])

    def post(self):
        """Create new electrovalve"""
        json = request.get_json()
        electrovalve, errors = ElectrovalveSchema().load(json)
        if errors:
            return make_response(jsonify({'message': errors}), 400)
        try:
            self.validatePin(electrovalve)
        except Forbidden as e:
            response = e.args[0]
            return make_response(response, 403)

        result = self.electrovalve_dao.createElectrovalve(electrovalve)
        electrovalve_id = str(result.inserted_id)

        if electrovalve['mode'] != 'manual':
            self.job_factory.makeJob(electrovalve['mode']).add(electrovalve_id, electrovalve)

        return jsonify({'id': electrovalve_id})
