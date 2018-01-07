from flask_restful import Resource
from flask import jsonify, make_response

from waterberry.facade.job_facade import JobFacade
from waterberry.facade.pin_facade import PinFacade
from waterberry.utils.messages import *

class ElectrovalveResource(Resource):
    def __init__(self, **kwargs):
        self.job_facade = JobFacade(kwargs['scheduler'])
        self.pin_facade = PinFacade(kwargs['mongo'])

    def __isPinAlreadyInUse(self, property, json, data):
        available_pins = map(lambda pin : pin, self.pin_facade.getAvailablePin())
        if data is None:
            return json[property] not in available_pins
        else:
            return json[property] != data[property] and json[property] not in available_pins

    def validatePin(self, electrovalve, data=None):
        if self.__isPinAlreadyInUse('electrovalve_pin', electrovalve, data):
            return make_response(jsonify({'message':
                ELECTROVALVE_PIN_ALREADY_IN_USE.format(electrovalve['electrovalve_pin'])}), 403)

        if electrovalve['mode'] == 'automatic':
            if self.__isPinAlreadyInUse('sensor_pin', electrovalve, data):
                return make_response(jsonify({'message':
                    SENSOR_PIN_ALREADY_IN_USE.format(electrovalve['sensor_pin'])}), 403)

    def isWatering(self, data):
        if data['watering']:
            return make_response(jsonify({'message': ELECTROVALVE_IS_WATERING }), 403)

    def addManualJob(self, electrovalve_id):
        self.job_facade.addManualJob(electrovalve_id)

    def removeJob(self, electrovalve, electrovalve_id):
        if electrovalve['mode'] == 'manual':
            self.job_facade.removeManualJob(electrovalve_id)
        elif electrovalve['mode'] == 'automatic':
            self.job_facade.removeAutomaticJob(electrovalve_id)
        elif electrovalve['mode'] == 'scheduled':
            for count, calendar in enumerate(electrovalve['timetable']):
                self.job_facade.removeScheduledJob(count, electrovalve_id)

    def addJob(self, electrovalve, electrovalve_id):
        if electrovalve['mode'] == 'manual':
            self.job_facade.removeManualJob(electrovalve_id)
            self.job_facade.addManualJob(electrovalve_id)
        elif electrovalve['mode'] == 'automatic':
            self.job_facade.removeAutomaticJob(electrovalve_id)
            self.job_facade.addAutomaticJob(electrovalve_id)
        elif electrovalve['mode'] == 'scheduled':
            for count, calendar in enumerate(electrovalve['timetable']):
                self.job_facade.removeScheduledJob(count, electrovalve_id)
                self.job_facade.addScheduledJob(count, calendar, electrovalve_id)
