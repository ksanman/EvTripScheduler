class Stop:
    def __init__(self, order, name, energyExpended, timeFromPreviousStop, chargerConnection=None):
        self.Order = order
        self.Name = name
        self.EnergyExpended = energyExpended
        self.TimeFromPreviousStop = timeFromPreviousStop
        self.ChargerConnection = chargerConnection