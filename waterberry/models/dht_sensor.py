
class DHTSensor(object):
    def __init__(self, **kwargs):
        self.selected = kwargs['selected']
        self.types = kwargs['types']
        self.pin = None if 'pin' not in kwargs else kwargs['pin']
        self.humidity = None if 'humidity' not in kwargs else kwargs['humidity']    
        self.temperature = None if 'temperature' not in kwargs else kwargs['temperature']