
class DHTSensor(object):
    def __init__(self, **kwargs):
        self.selected = None if 'selected' not in kwargs else kwargs['selected']
        self.types = None if 'types' not in kwargs else kwargs['types']
        self.pin = None if 'pin' not in kwargs else kwargs['pin']
        self.humidity = None if 'humidity' not in kwargs else kwargs['humidity']    
        self.temperature = None if 'temperature' not in kwargs else kwargs['temperature']
