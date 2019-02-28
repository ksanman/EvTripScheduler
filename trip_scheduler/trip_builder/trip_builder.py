from trip import Trip
from vehicle import SimpleVehicle, NissanLeaf

class TripBuilder:
    def BuildTrip(self, expectedTripTime, batteryCapacity, vehicle):
        self.Vehicle = self.GetVehicle(batteryCapacity, vehicle)
        numberOfStops = self.GetNumberOfStops()
        hasDestinationCharger = self.GetHasDestinationCharger()
        route = self.GetRoute()
        
        return Trip(numberOfStops=numberOfStops, expectedTripTime=expectedTripTime, batteryCapacity=self.Vehicle.BatteryCapacity\
            , hasDestinationCharger=hasDestinationCharger, route=route, vehicle=self.Vehicle)

    def GetVehicle(self, batteryCapacity, vehicle):
        if vehicle == 'SimpleVehicle':
            return SimpleVehicle(batteryCapacity)
        if vehicle == 'NissanLeaf':
            return NissanLeaf(batteryCapacity)

    def GetNumberOfStops(self):
        return None
    
    def GetHasDestinationCharger(self):
        return None

    def GetRoute(self):
        return None