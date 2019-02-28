class ChargerConnection:
    def __init__(self, price, power=None, current=None, voltage=None):
        hasCurrentAndVoltage = (current is not None and voltage is not None)
        hasPower = (power is not None)
        if not hasCurrentAndVoltage and not hasPower:
            raise Exception("Must provider current and voltage or power.")
        
        if hasPower:
            self.Power = power
        else:
            self.Power = (current * voltage)/ 1000

        self.Price = price