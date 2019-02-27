class Stop:
    def __init__(self, energyExpended, timeFromPreviousStop, chargerConnection=None):
        self.EnergyExpended = energyExpended
        self.TimeFromPreviousStop = timeFromPreviousStop
        self.ChargerConnection = chargerConnection