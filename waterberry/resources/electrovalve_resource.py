from flask_restful import Resource
from flask import jsonify, make_response

from waterberry.utils.messages import DUPLICATE_PINS, ELECTROVALVE_PIN_ALREADY_IN_USE, ELECTROVALVE_IS_WATERING
from waterberry.utils.logger import logger

class Forbidden(Exception):
    pass

class ElectrovalveResource(Resource):
    def __init__(self, **kwargs):
        self.electrovalve_dao = kwargs['electrovalve_dao']
        self.raspberry_dao = kwargs['raspberry_dao']        
        self.dht_sensor_dao = kwargs['dht_sensor_dao']
        self.job_factory = kwargs['job_factory']
        self.board = kwargs['board']
        self.raspberry = kwargs['raspberry']

    def validatePin(self, current_electrovalve):
        sensor = self.dht_sensor_dao.getSensor()
        electrovalves = self.electrovalve_dao.getElectrovalveList()
        raspberry = self.raspberry_dao.getRasberry()

        used_pins = []
        for electrovalve in electrovalves:
            used_pins = used_pins + electrovalve.getUsedPins()
        used_pins.append(sensor.pin)

        available_pins = list(set(raspberry.getPinList()) - set(used_pins))
        pins = current_electrovalve.getUsedPins()

        if electrovalve.mode == 'automatic' and len(pins) < 5:
            message = DUPLICATE_PINS.format(electrovalve.getUsedPins())
            raise Forbidden(jsonify({'message': message}))

        for pin in pins:
            if pin not in available_pins:
                logger.pin('pin already in use ...')
                message = ELECTROVALVE_PIN_ALREADY_IN_USE.format(pin)
                raise Forbidden(jsonify({'message': message}))

    def isWatering(self, electrovalve):
        if electrovalve.watering:
            message = ELECTROVALVE_IS_WATERING
            raise Forbidden(jsonify({'message': message}))

    def cleanBoard(self, electrovalve):
        pin = self.raspberry.getPinByName(electrovalve.getUsedPins())
        self.board.cleanupPin(pin)