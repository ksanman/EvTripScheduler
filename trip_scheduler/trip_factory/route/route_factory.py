from ..location import Address, Connection, Location, Charger as DbCharger
from route import LinearRoute

class RouteFactory:
    def BuildRoute(self, tripParameters):
        if tripParameters.NumberOfChargers != 0:
            return self.BuildLinearRoute(tripParameters)
        elif len(tripParameters.Distances) > 0:
            return self.BuildRouteFromDistances(tripParameters)
        elif len(tripParameters.Filenames) > 0:
            return self.BuildRouteFromFilenames(tripParameters)
        else:
            return self.BuildRouteFromOsrm(tripParameters)

    def BuildLinearRoute(self, tripParameters):
        return LinearRoute(range(tripParameters.NumberOfChargers), tripParameters.HasDestinationCharger, trip.Car)

    def BuildRouteFromDistances(self, tripParameters):
        pass

    def BuildRouteFromFilenames(self, tripParameters):
        pass

    def BuildRouteFromOsrm(self, tripParameters):
        pass
        