from stop import Stop

class Charger(stop):
    def __init__(self, location, distanceFromPreviousLocation, timeFromPreviousLocation, energyExpended, distanceFromRoute):
        self.DistanceFromRoute = distanceFromRoute
        super(Charger, self).__init__(location, distanceFromPreviousLocation, timeFromPreviousLocation, energyExpended)