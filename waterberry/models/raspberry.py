
class Raspberry(object):
    def __init__(self, id, name, gpio):
        self.id = id
        self.name = name
        self.gpio = gpio

    def getPinList(self):
        return [name for name, pin in self.gpio.iteritems()]

    def getPinByName(self, name):
        return self.gpio[name]
