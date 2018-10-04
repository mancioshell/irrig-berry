
class DHTSensor(object):
    def __init__(self, **kwargs):        
        self.type = kwargs['type']
        self.types = kwargs['types']
        self.pin = kwargs['pin']
        self.humidity = kwargs['humidity']    
        self.temperature = kwargs['temperature']