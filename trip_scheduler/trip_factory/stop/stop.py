class Stop(object):
    def __init__(self, location, distanceFromPreviousLocation, timeFromPreviousLocation, energyExpended):
        self.Location = location
        self.DistanceFromPreviousLocation = distanceFromPreviousLocation
        self.TimeFromPreviousLocation = timeFromPreviousLocation
        self.EnergyExpended = energyExpended