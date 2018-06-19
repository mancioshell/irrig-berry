from datetime import datetime
from marshmallow import fields, Schema, post_load, validates, validates_schema, ValidationError

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
    pin_di = fields.String(required=False)
    pin_do = fields.String(required=False)
    pin_clk = fields.String(required=False)
    pin_cs = fields.String(required=False)
    timetable = fields.Nested(TimetableSchema, many=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_object(self, data):
        logger.info(not 'timetable' in data)

        if data['mode'] == 'automatic' and not 'pin_di' in data:
            raise ValidationError('Automatic mode requires pin_di field')
        if data['mode'] == 'automatic' and not 'pin_do' in data:
            raise ValidationError('Automatic mode requires pin_do field')
        if data['mode'] == 'automatic' and not 'pin_clk' in data:
            raise ValidationError('Automatic mode requires pin_clk field')
        if data['mode'] == 'automatic' and not 'pin_cs' in data:
            raise ValidationError('Automatic mode requires pin_cs field')

        if data['mode'] == 'automatic' and not 'humidity_threshold' in data:
            raise ValidationError('Automatic mode requires humidity_threshold field')

        if data['mode'] != 'automatic' and 'pin_di' in data:
            raise ValidationError('pin_di field is valid only for automatic mode')
        if data['mode'] != 'automatic' and 'pin_do' in data:
            raise ValidationError('pin_do field is valid only for automatic mode')
        if data['mode'] != 'automatic' and 'pin_clk' in data:
            raise ValidationError('pin_clk field is valid only for automatic mode')
        if data['mode'] != 'automatic' and 'pin_cs' in data:
            raise ValidationError('pin_cs field is valid only for automatic mode')

        if data['mode'] != 'automatic' and 'humidity_threshold' in data:
            raise ValidationError('humidity_threshold field is valid only for automatic mode')

        if data['mode'] == 'scheduled' and not 'timetable' in data:
            raise ValidationError('Scheduled mode requires timetable field')
        if data['mode'] != 'scheduled' and 'timetable' in data:
            raise ValidationError('timetable field is valid only for scheduled mode')

class DHTSensorSchema(Schema):
    type = fields.String(required=True, validate=lambda x: x in ['DHT11', 'DHT22', 'AM2302'])
    pin = fields.String(required=True)
