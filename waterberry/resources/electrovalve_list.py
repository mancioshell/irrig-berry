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
        electrovalves = self.electrovalve_dao.getAllElectrovalves()
        return jsonify(electrovalves)

    def delete(self):
        """Delete all electrovalves"""
        electrovalves = self.electrovalve_dao.getAllElectrovalves()
        for electrovalve in electrovalves:
            self.job_factory.makeJob(electrovalve).remove()

        self.electrovalve_dao.deleteAllElectrovalves()
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

        electrovalve_id = self.electrovalve_dao.createElectrovalve(electrovalve)        

        if electrovalve.mode != 'manual':
            self.job_factory.makeJob(electrovalve).add()

        return jsonify({'id': electrovalve_id})
