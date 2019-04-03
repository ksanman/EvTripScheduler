class TripParameters:
    def __init__(self, expectedTripTime, batteryCapacity, vehicle, numberOfStops=None, routeFileName=None, chargersFileName=None, hasDestinationCharger=None,startPoint=None, endPoint=None, tripName=''):
        self.ExpectedTripTime = expectedTripTime
        self.BatteryCapacity = batteryCapacity
        self.Vehicle = vehicle
        self.NumberOfStops = numberOfStops
        self.RouteFileName = routeFileName
        self.ChargerFileName = chargersFileName
        self.StartPoint = startPoint
        self.EndPoint = endPoint
        self.HasDestinationCharger = hasDestinationCharger
        self.TripName = tripName