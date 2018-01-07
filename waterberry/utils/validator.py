from datetime import datetime
from marshmallow import fields, Schema, post_load, validates, validates_schema, ValidationError

from waterberry.facade.pin_facade import PinFacade
from waterberry.utils.logger import logger

class TimetableSchema(Schema):
    day = fields.String(required=True, validate=lambda x: x in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])
    time = fields.String(required=True)

    @validates('time')
    def validate_time(self, value):
        try:
            datetime.strptime(value,'%H:%M')
        except ValueError:
            logger.error('Time must be a time in this format:  H:M')
            raise ValidationError('Time must be a time in this format:  H:M')

class ElectrovalveSchema(Schema):
    name = fields.String(required=True)
    mode = fields.String(required=True, validate=lambda x: x in ['manual', 'automatic', 'scheduled'])
    electrovalve_pin = fields.String(required=True)
    duration = fields.Integer(required=True)
    humidity_threshold = fields.Integer(required=False)
    sensor_pin = fields.String(required=False)
    timetable = fields.Nested(TimetableSchema, many=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_object(self, data):
        logger.info(not 'timetable' in data)
        if data['mode'] == 'automatic' and not 'sensor_pin' in data:
            raise ValidationError('Automatic mode requires sensor_pin field')
        if data['mode'] == 'automatic' and not 'humidity_threshold' in data:
            raise ValidationError('Automatic mode requires humidity_threshold field')

        if data['mode'] != 'automatic' and 'sensor_pin' in data:
            raise ValidationError('sensor_pin field is valid only for automatic mode')
        if data['mode'] != 'automatic' and 'humidity_threshold' in data:
            raise ValidationError('humidity_threshold field is valid only for automatic mode')

        if data['mode'] == 'scheduled' and not 'timetable' in data:
            raise ValidationError('Scheduled mode requires timetable field')
        if data['mode'] != 'scheduled' and 'timetable' in data:
            raise ValidationError('timetable field is valid only for scheduled mode')
