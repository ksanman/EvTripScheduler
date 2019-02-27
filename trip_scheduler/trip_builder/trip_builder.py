from ..trip import Trip

class TripBuilder:
    def BuildTrip(self, expectedTripTime, vehicle):
        numberOfStops = self.GetNumberOfStops()
        hasDestinationCharger = self.GetHasDestinationCharger()
        route = self.GetRoute()
        
        return Trip(numberOfStops=numberOfStops, expectedTripTime=expectedTripTime, batteryCapacity=vehicle.BatteryCapacity\
            , hasDestinationCharger=hasDestinationCharger, route=route, vehicle=vehicle)

    def GetNumberOfStops(self):
        return None
    
    def GetHasDestinationCharger(self):
        return None

    def GetRoute(self):
        return None