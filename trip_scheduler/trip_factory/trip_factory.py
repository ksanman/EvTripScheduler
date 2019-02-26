from route_factory import RouteFactory
from possible_schedule import PossibleSchedule

class TripFactory:
    def __init__(self):
        self.RouteFactory = RouteFactory()

    def BuildPossibleSchedulesForTrips(self, tripParameters):
        for tripParameter in tripParameters:
            self.BuildPossibleTripSchedule(tripParameter)

    def BuildPossibleTripSchedule(self, tripParameter):
        route = RouteFactory.BuildRoute(tripParameter)

        return PossibleSchedule(route.Polyline, route.Coordinates, tripParameter.ExpectedTime, tripParameter.Car, route.PossibleStops)
