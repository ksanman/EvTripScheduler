from stop import Stop
from ...location import Charger

class Destination(Stop):
    def __init__(self, location, distanceFromPreviousLocation, timeFromPreviousLocation, energyExpended, distanceFromRoute):
        self.HasCharger = isinstance(location, Charger)
        self.DistanceFromRoute
        super(Destination, self).__init__(location, distanceFromPreviousLocation, timeFromPreviousLocation, energyExpended)