from trip_builder import TripBuilder
from ..stop import Stop
from ..charger_connection import ChargerConnection
from .route import Route

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
        route = [Stop(0, "Start", 1, 1, None)]

        for stop in range(1, self.NumberOfStops - 1, 1):
            route.append(Stop(stop, str(stop), 1, 1, ChargerConnection(0.13, 25)))

        if self.HasDestinationCharger:
            route.append(Stop(self.NumberOfStops-1, "Destination", 1, 1, ChargerConnection(0.13, 25)))
        else:
            route.append(Stop(self.NumberOfStops-1, "Destination", 1, 1, None))

        return Route(route)