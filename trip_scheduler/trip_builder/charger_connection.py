class ChargerConnection:
    def __init__(self, price, power=None, current=None, voltage=None):
        if not ((current and voltage) or power):
            raise Exception("Must provider current and voltage or power.")
        
        if power:
            self.Power = power
        else:
            self.Power = (current * voltage)/ 1000

        self.Price = price