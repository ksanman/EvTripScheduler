from trip_builder import TripBuilder
from charger_context import ChargerContext
from trip import Stop
from routing import Osrm
from trip import Coordinate
from trip import RoadSegment
from trip import ChargerConnection
from routing import Route
from ..utility import RoundUp

class DistanceTripBuilder(TripBuilder, object):
    def __init__(self, distances, hasDestinationCharger=None):
        self.NumberOfStops = len(distances) + 1
        self.Distances = distances
        self.HasDestinationCharger = hasDestinationCharger
        self.ChargerContext = ChargerContext()
        super(DistanceTripBuilder, self).__init__()

    def GetNumberOfStops(self):
        return self.NumberOfStops

    def GetHasDestinationCharger(self):
        return self.HasDestinationCharger

    def GetRoute(self):
        route = [Stop(0, "Start", 0, 0, 0, ChargerConnection(0,0))]

        if self.HasDestinationCharger:
            for i, stop in enumerate(self.Distances):
                chargerConnection = ChargerConnection(0.13, 50, 125, 400)
                distanceFromPrevious, durationFromPrevious = stop[0], stop[1]
                energyExpended = RoundUp(self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0)))
                route.append(Stop(stop, 'Charger_{0}'.format(i) , energyExpended, distanceFromPrevious, self.ConvertToTimeBlock(durationFromPrevious), chargerConnection))

        else:
            for i, stop in enumerate(self.Distances):
                chargerConnection = ChargerConnection(0.13, 50, 125, 400)
                distanceFromPrevious, durationFromPrevious = stop[0], stop[1]
                energyExpended = RoundUp(self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0)))
                route.append(Stop(stop, 'Charger_{0}'.format(i) , energyExpended, distanceFromPrevious, self.ConvertToTimeBlock(durationFromPrevious), chargerConnection))

            chargerConnection = ChargerConnection(0.13, 50, 125, 400)
            distanceFromPrevious, durationFromPrevious = self.Distances[-1][0], self.Distances[-1][1]
            energyExpended = RoundUp(self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0)))
            route.append(Stop(stop, 'Destination', energyExpended, distanceFromPrevious, self.ConvertToTimeBlock(durationFromPrevious), chargerConnection))

        return Route(route, '', [])