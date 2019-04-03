from trip import Trip
from vehicle import SimpleVehicle, NissanLeaf
from ..utility import RoundUp

class TripBuilder:
    def BuildTrip(self, expectedTripTime, batteryCapacity, vehicle, timeBlockConstant, tripName=''):
        self.TimeBlockConstant = timeBlockConstant
        self.Vehicle = self.GetVehicle(batteryCapacity, vehicle)
        numberOfStops = self.GetNumberOfStops()
        hasDestinationCharger = self.GetHasDestinationCharger()
        route = self.GetRoute()
        
        return Trip(numberOfStops=numberOfStops, expectedTripTime=expectedTripTime, batteryCapacity=self.Vehicle.BatteryCapacity\
            , hasDestinationCharger=hasDestinationCharger, route=route, vehicle=self.Vehicle, tripName=tripName)

    def GetVehicle(self, batteryCapacity, vehicle):
        if vehicle == 'SimpleVehicle':
            return SimpleVehicle(batteryCapacity, self.TimeBlockConstant)
        if vehicle == 'NissanLeaf':
            return NissanLeaf(batteryCapacity, self.TimeBlockConstant)

    def GetNumberOfStops(self):
        return None
    
    def GetHasDestinationCharger(self):
        return None

    def GetRoute(self):
        return None

    def ConvertToTimeBlock(self, seconds):
        minutes = seconds / 60
        return RoundUp(minutes / self.TimeBlockConstant)