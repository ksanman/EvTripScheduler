from route import Route

class PredefinedRoute(Route):

    def __init__(self, distances, hasDestinationCharger):
        self.Distances = distances
        self.HasDestinationCharger = hasDestinationCharger
        super(PredefinedRoute, self).__init__()

    def GetRoute(self):
        return '', self.Distances

    def GetPossibleChargingStops(self, coordinates):
        from ...location import Charger, Connection
        
        possibleChargeringStops = []
        for possibleChargingLocation in coordinates:
            possibleChargeringStops.append(Charger(0, "", None, [Connection(0, 25, 63, 400)], 0.13, None))

        return possibleChargeringStops

    def GetStart(self):
        from ..stop import Start
        return Start(None)

    def GetCharger(self, stop):
        from ..stop import Charger
        return Charger(stop, stop, stop, -stop, stop)

    def GetDestination(self):
        from ..stop import Destination
        if self.HasDestinationCharger:
            from ...location import Charger, Connection
            charger = Charger(0, "", None, [Connection(0, 25, 63, 400)], 0.13, None)
            return Destination(charger, self.LinearDistance, self.LinearTime, self.LinearEnergyExpended, self.LinearDistanceFromRoute)
        else:
            return Destination(None, self.LinearDistance, self.LinearTime, self.LinearEnergyExpended)