from battery import Battery

class SimpleBattery(Battery):
    def __init__(self, capacity):
        super(SimpleBattery, self).__init__(capacity)