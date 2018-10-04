
class Raspberry(object):
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.gpio = kwargs['gpio']

    def getPinList(self):
        return [name for name in self.gpio.iteritems()]

    def getPinByName(self, names):
        if type(names) is list:
            pins = []
            for name in names:
                pins.append(self.gpio[name])
            return pins
        else:
            return self.gpio[names]
