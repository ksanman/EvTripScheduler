from route import Route

class LinearRoute(Route):
    
    LinearDistance = 1
    LinearTime = 1
    LinearEnergyExpended = -1
    LinearDistanceFromRoute = 1

    def __init__(self, numberOfStops, hasDestinationCharger):
        self.NumberOfStops = numberOfStops
        self.HasDestinationCharger = hasDestinationCharger
        super(LinearRoute, self).__init__()

    def GetRoute(self):
        return '', range(self.NumberOfStops)

    def GetPossibleChargingStops(self, coordinates):
        from ...location import Charger, Connection
        
        possibleChargeringStops = []
        for possibleChargingLocation in coordinates:
            possibleChargeringStops.append(Charger(0, "", None, [Connection(0, 25, 63, 400)], 0.13, None))

        return possibleChargeringStops

    def GetStart(self):
        from ..stop import Start
        return Start(None)

    def GetDestination(self):
        from ..stop import Destination
        if self.HasDestinationCharger:
            from ...location import Charger, Connection
            charger = Charger(0, "", None, [Connection(0, 25, 63, 400)], 0.13, None)
            return Destination(charger, self.LinearDistance, self.LinearTime, self.LinearEnergyExpended, self.LinearDistanceFromRoute)
        else:
            return Destination(None, self.LinearDistance, self.LinearTime, self.LinearEnergyExpended)