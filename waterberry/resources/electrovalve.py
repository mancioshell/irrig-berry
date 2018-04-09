from datetime import datetime

from flask_restful import Resource
from flask import request, jsonify, make_response
from bson.objectid import ObjectId

from waterberry.facade.gpio_facade import GPIOFacade
from waterberry.facade.pin_facade import PinFacade
from waterberry.resources.electrovalve_resource import ElectrovalveResource
from waterberry.utils.validator import ElectrovalveSchema
from waterberry.utils.messages import *
from waterberry.utils.logger import logger

class Electrovalve(ElectrovalveResource):
    def __init__(self, **kwargs):
        self.mongo = kwargs['mongo']
        self.scheduler = kwargs['scheduler']
        self.pin_facade = PinFacade(kwargs['mongo'])
        super(Electrovalve, self).__init__(**kwargs)

    def __toObjectId(self, id):
        return ObjectId(id)

    def get(self, electrovalve_id):
        """Get electrovalve"""
        _id = self.__toObjectId(electrovalve_id)
        electrovalve = self.mongo.db.electrovalve.find_one({'_id': _id})
        if electrovalve is not None:
            return jsonify(electrovalve)
        else:
            return make_response(jsonify({'message': ELECTROVALVE_NOT_FOUND.format(electrovalve_id)}), 404)

    def delete(self, electrovalve_id):
        """Delete electrovalve"""
        _id = self.__toObjectId(electrovalve_id)
        electrovalve = self.mongo.db.electrovalve.find_one_and_delete({'_id': _id})
        if electrovalve is not None:
            electrovalve_pin = self.pin_facade.getPinIdFromName(electrovalve['electrovalve_pin'])
            GPIOFacade().initBoard()
            GPIOFacade().cleanupPin(electrovalve_pin)

            if electrovalve['mode'] == 'automatic':
                sensor_pin = self.pin_facade.getPinIdFromName(electrovalve['sensor_pin'])
                GPIOFacade().cleanupPin(sensor_pin)

            self.removeJob(electrovalve, electrovalve_id)
            return jsonify({})
        else:
            return make_response(jsonify({'message': ELECTROVALVE_NOT_FOUND.format(electrovalve_id)}), 404)

    def put(self, electrovalve_id):
        """Update electrovalve"""
        _id = self.__toObjectId(electrovalve_id)
        json = request.get_json()
        electrovalve, errors = ElectrovalveSchema().load(json)
        if errors:
            return make_response(jsonify({'message': errors}), 400)

        GPIOFacade().initBoard()

        result = self.mongo.db.electrovalve.find_one({'_id': _id })
        if result is not None:
            self.isWatering(result)
            self.validatePin(electrovalve, result)
            electrovalve_pin = self.pin_facade.getPinIdFromName(result['electrovalve_pin'])
            GPIOFacade().cleanupPin(electrovalve_pin)
            if result['mode'] == 'automatic':
                sensor_pin = self.pin_facade.getPinIdFromName(result['sensor_pin'])
                GPIOFacade().cleanupPin(sensor_pin)
        else:
            return make_response(jsonify({'message': ELECTROVALVE_NOT_FOUND.format(electrovalve_id)}), 404)

        electrovalve_pin = self.pin_facade.getPinIdFromName(electrovalve['electrovalve_pin'])
        GPIOFacade().setupOutputPin(electrovalve_pin)
        GPIOFacade().disablePin(electrovalve_pin)

        if electrovalve['mode'] == 'automatic':
            sensor_pin = self.pin_facade.getPinIdFromName(electrovalve['sensor_pin'])
            GPIOFacade().setupInputPin(sensor_pin)
            electrovalve['timetable'] = None
        elif electrovalve['mode'] == 'scheduled':
            electrovalve['humidity_threshold'] = None
            electrovalve['sensor_pin'] = None
        else:
            electrovalve['timetable'] = None
            electrovalve['humidity_threshold'] = None
            electrovalve['sensor_pin'] = None

        self.mongo.db.electrovalve.update_one({'_id': _id}, {"$set":  electrovalve})
        if electrovalve['mode'] != 'manual':
            self.addJob(electrovalve, electrovalve_id)
        return make_response(jsonify({'id': electrovalve_id}), 201)

    def patch(self, electrovalve_id):
        """Update electrovalve state"""
        _id = self.__toObjectId(electrovalve_id)
        result = self.mongo.db.electrovalve.find_one({'_id': _id })
        electrovalve = {'mode': 'manual'}
        self.isWatering(result)
        self.addJob(electrovalve, electrovalve_id)
        return make_response(jsonify({'id': electrovalve_id}), 201)
