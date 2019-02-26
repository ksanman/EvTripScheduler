from ..stop import Charger, Destination

class Route(object):
    def __init__(self, car):
        self.Car = car
        coordinates, polyline = self.GetRoute()
        self.PossibleChargingStops = self.GetPossibleChargingStops(coordinates)
        possibleStops = self.GetPossibleStops()
        self.Polyline = polyline
        self.Coordinates = coordinates
        self.PossibleStops = possibleStops

    def GetPossibleStops(self):
        start = self.PossibleChargingStops[0]
        chargingPoints = self.PossibleChargingStops[1:-1]
        destination = self.PossibleChargingStops[-1]

        route = [self.GetStart(start)]

        for stop in chargingPoints:
           
            route.append(self.GetCharger(stop))
        
        route.append(self.GetDestination(destination))

        return route

    def GetCharger(self, stop):   
        distance, time, energyExpended, distanceFromRoute, durationFromRoute, energyExpendedFromRoute = self.GetTripInformation(stop)  
        return Charger(stop, distance, time, energyExpended, distanceFromRoute)

    def GetDestination(self, destination):
        distance, time, energyExpended, distanceFromRoute, durationFromRoute, energyExpendedFromRoute = self.GetTripInformation(destination)
        if self.HasDestinationCharger:
            from ...location import Charger, Connection
            charger = Charger(0, "", None, [Connection(0, 25, 63, 400)], 0.13, None)
            return Destination(charger, self.LinearDistance, self.LinearTime, self.LinearEnergyExpended, self.LinearDistanceFromRoute)
        else:
            return Destination(None, self.LinearDistance, self.LinearTime, self.LinearEnergyExpended)

    def GetTripInformation(self, stop):
        distance, duration = self.GetDistanceAndDuration()
        energyExpended = self.Car.Drive(distance, duration)
        distanceFromRoute, durationFromRoute = self.GetDistanceAndDurationFromRoute()
        energyExpendedFromRoute = self.Car.Drive(distanceFromRoute, durationFromRoute)
        
        return (distance, duration, energyExpended, distanceFromRoute, durationFromRoute, energyExpendedFromRoute)

