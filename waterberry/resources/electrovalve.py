from datetime import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response

from waterberry.resources.electrovalve_resource import ElectrovalveResource, Forbidden
from waterberry.utils.validator import ElectrovalveSchema
from waterberry.utils.messages import *
from waterberry.utils.logger import logger

class Electrovalve(ElectrovalveResource):
    def __init__(self, **kwargs):
        super(Electrovalve, self).__init__(**kwargs)

    def get(self, electrovalve_id):
        """Get electrovalve"""
        electrovalve = self.electrovalve_dao.getElectrovalveById(electrovalve_id)
        if electrovalve is not None:
            return jsonify(electrovalve)
        else:
            return make_response(jsonify({'message': ELECTROVALVE_NOT_FOUND.format(electrovalve_id)}), 404)

    def delete(self, electrovalve_id):
        """Delete electrovalve"""
        electrovalve = self.electrovalve_dao.deleteElectrovalveById(electrovalve_id)
        if electrovalve is not None:
            self.job_factory.makeJob(electrovalve).remove()
            return jsonify({})
        else:
            return make_response(jsonify({'message': ELECTROVALVE_NOT_FOUND.format(electrovalve_id)}), 404)

    def put(self, electrovalve_id):
        """Update electrovalve"""
        json = request.get_json()
        electrovalve, errors = ElectrovalveSchema().load(json)
        if errors:
            return make_response(jsonify({'message': errors}), 400)

        electrovalve.id = electrovalve_id
        current_electrovalve = self.electrovalve_dao.getElectrovalveById(electrovalve_id)

        if current_electrovalve is not None:
            try:
                self.isWatering(current_electrovalve)
                self.validatePin(electrovalve, current_electrovalve)
            except Forbidden as e:
                response = e.args[0]
                return make_response(response, 403)
            self.job_factory.makeJob(current_electrovalve).remove()
        else:
            return make_response(jsonify({'message': ELECTROVALVE_NOT_FOUND.format(electrovalve_id)}), 404)
       
        self.electrovalve_dao.updateElectrovalveById(electrovalve)
        if electrovalve.mode != 'manual':
            self.job_factory.makeJob(electrovalve).add()

        return make_response(jsonify({'id': electrovalve_id}), 201)

    def patch(self, electrovalve_id):
        """Update electrovalve state"""
        electrovalve = self.electrovalve_dao.getElectrovalveById(electrovalve_id)        
        try:
            self.isWatering(result)
        except Forbidden as e:
            response = e.args[0]
            return make_response(response, 403)
        self.job_factory.makeJob(electrovalve).add()
        return make_response(jsonify({'id': electrovalve_id}), 201)
