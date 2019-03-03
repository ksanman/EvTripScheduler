from trip_builder import TripBuilder
from trip import Stop
from trip import ChargerConnection
from routing import Route

class SimpleTripBuilder(TripBuilder, object):
    def __init__(self, numberOfStops, hasDestinationCharger):
        self.NumberOfStops = numberOfStops
        self.HasDestinationCharger = hasDestinationCharger
        super(SimpleTripBuilder, self).__init__()

    def GetNumberOfStops(self):
        return self.NumberOfStops
    
    def GetHasDestinationCharger(self):
        return self.HasDestinationCharger

    def GetRoute(self):
        route = [Stop(0, "Start", 0, 0, 0, ChargerConnection(0,0))]

        for stop in range(1, self.NumberOfStops - 1, 1):
            route.append(Stop(stop, str(stop), 1, 1, 1, ChargerConnection(0.13, 25)))

        if self.HasDestinationCharger:
            route.append(Stop(self.NumberOfStops-1, "Destination", 1, 1, 1, ChargerConnection(0.13, 25)))
        else:
            route.append(Stop(self.NumberOfStops-1, "Destination", 1, 1, 1, None))

        return Route(route)