class ElectrovalveFactory:
    def __init__(self, mode):
        self.mode = mode
        
    def createElectrovalve(self, **kwargs):
        switcher = {
            'manual': ManualElectrovalve(**kwargs),
            'automatic': AutomaticElectrovalve(**kwargs),
            'scheduled': ScheduledElectrovalve(**kwargs)
        }
        return switcher.get(self.mode, ManualElectrovalve(**kwargs))


class Electrovalve(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.id = kwargs['_id']        
        self.watering = False
        self.next_water = None
        self.last_water = None

class ManualElectrovalve(Electrovalve):
    def __init__(self, **kwargs):
        super(ManualElectrovalve, self).__init__(kwargs)
        self.electrovalve_pin = kwargs['electrovalve_pin']
        self.duration = kwargs['duration']

    def getUsedPins(self):
        return [self.electrovalve_pin]

class ScheduledElectrovalve(ManualElectrovalve):
    def __init__(self, **kwargs):
        super(ScheduledElectrovalve, self).__init__(kwargs)
        self.timetable = kwargs['timetable']

class AutomaticElectrovalve(ManualElectrovalve):
    def __init__(self, **kwargs):
        super(AutomaticElectrovalve, self).__init__(kwargs)
        self.humidity_threshold = kwargs['humidity_threshold']
        self.pin_di = kwargs['pin_di']
        self.pin_do = kwargs['pin_do']
        self.pin_clk = kwargs['pin_clk']
        self.pin_cs = kwargs['pin_cs']

    def getUsedPins(self):
        return super(AutomaticElectrovalve, self).getUsedPins() + [self.pin_di, self.pin_do, self.pin_clk, self.pin_cs]
