class Trip:
    def __init__(self, numberOfStops=None, expectedTripTime=None, batteryCapacity=None, hasDestinationCharger=None, route=None, vehicle=None):
        self.NumberOfStops = numberOfStops
        self.ExpectedTripTime = expectedTripTime
        self.BatteryCapacity  = batteryCapacity
        self.HasDestinationCharger = hasDestinationCharger
        self.Vehicle = vehicle
        self.Route = route