class Stop:
    def __init__(self, order, name, energyExpended, distanceFromPreviousStop, timeFromPreviousStop, chargerConnection=None):
        self.Order = order
        self.Name = name
        self.DistanceFromPreviousStop = distanceFromPreviousStop
        self.EnergyExpended = energyExpended
        self.TimeFromPreviousStop = timeFromPreviousStop
        self.ChargerConnection = chargerConnection