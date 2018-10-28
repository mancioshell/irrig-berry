
class DHTSensor(object):
    def __init__(self, selected = None, types = None, pin = None, humidity = None, temperature = None):
        self.selected = selected
        self.types = types
        self.pin = pin
        self.humidity = humidity   
        self.temperature = temperature