from flask_restful import Resource
from flask import jsonify, make_response

from waterberry.utils.messages import *
from waterberry.utils.logger import logger

class Forbidden(Exception):
    pass

class ElectrovalveResource(Resource):
    def __init__(self, **kwargs):
        self.electrovalve_dao = kwargs['electrovalve_dao']
        self.raspberry_dao = kwargs['raspberry_dao']
        self.job_factory = kwargs['job_factory']
        self.dht_sensor_dao = kwargs['dht_sensor_dao']

    def validatePin(self, electrovalve, data=None):
        dht_sensor_pin = self.dht_sensor_dao.getSensor()['pin']
        electrovalves = self.electrovalve_dao.getElectrovalveList()
        available_pins = self.raspberry_dao.getAvailablePinList(electrovalves, dht_sensor_pin)

        current_electovalve_pin = None
        current_pin_di = None
        current_pin_do = None
        current_pin_clk = None
        current_pin_cs = None
        if data is not None:
            current_pin_di = data['pin_di'] if 'pin_di' in data else None
            current_pin_do = data['pin_do'] if 'pin_do' in data else None
            current_pin_clk = data['pin_clk'] if 'pin_clk' in data else None
            current_pin_cs = data['pin_cs'] if 'pin_cs' in data else None
            current_electovalve_pin = data['electrovalve_pin'] if 'electrovalve_pin' in data else None

        electrovalve_pin = electrovalve['electrovalve_pin']
        pin_di = electrovalve['pin_di'] if 'pin_di' in electrovalve else None
        pin_do = electrovalve['pin_do'] if 'pin_do' in electrovalve else None
        pin_clk = electrovalve['pin_clk'] if 'pin_clk' in electrovalve else None
        pin_cs = electrovalve['pin_cs'] if 'pin_cs' in electrovalve else None

        logger.info('electrovalve_pin : {}'.format(electrovalve_pin))
        logger.info('pin_di : {}'.format(pin_di))
        logger.info('pin_do : {}'.format(pin_do))
        logger.info('pin_clk : {}'.format(pin_clk))
        logger.info('pin_cs : {}'.format(pin_cs))

        logger.info('available_pins : {}'.format(available_pins))

        data_pin_list = set([current_electovalve_pin, current_pin_di, current_pin_do, current_pin_clk, current_pin_cs])
        electrovalve_pin_list = set([electrovalve_pin, pin_di, pin_do, pin_clk, pin_cs])

        if electrovalve['mode'] == 'automatic' and len(electrovalve_pin_list) < 5:
            message = DUPLICATE_PINS.format(electrovalve_pin_list)
            raise Forbidden(jsonify({'message': message}))

        for pin in electrovalve_pin_list:
            if pin is not None and pin not in available_pins + list(data_pin_list):
                logger.pin('pin already in use ...')
                message = ELECTROVALVE_PIN_ALREADY_IN_USE.format(electrovalve_pin)
                raise Forbidden(jsonify({'message': message}))

    def isWatering(self, electrovalve):
        if electrovalve['watering']:
            message = ELECTROVALVE_IS_WATERING
            raise Forbidden(jsonify({'message': message}))
