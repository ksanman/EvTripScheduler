from trip_builder import SimpleTripBuilder, FileTripBuilder, OsrmTripBuilder
from environment import SimpleEnvironment, EvTripScheduleEnvironment
from optimizer import Optimizer

class TripScheduler:
    def __init__(self, timeBlockConstant=15):
        self.Optimizer = Optimizer(timeBlockConstant)
        self.TimeBlockConstant = timeBlockConstant

    def Schedule(self, parameters):
        if parameters.NumberOfStops:
            # Plan a simple trip
            return self.ScheduleSimpleTrip(parameters)
        elif parameters.RouteFileName:
            # Plan a trip with a file
            return self.ScheduleFileTrip(parameters)
        else:
            # Plan a trip using osrm and the database
            return self.ScheduleOsrmTrip(parameters)
    
    def ScheduleTrip(self, expectedTime, batteryCapacity, vehicle, environment, tripName):
        trip = self.TripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle, self.TimeBlockConstant, tripName)
        env = environment(trip)
        expectedValues = self.Optimizer.ComputeExpectedValue(env)
        policy = self.Optimizer.GetOptimalPolicy(expectedValues, env)
        schedule = self.Optimizer.GetSchedule(policy, trip, env)
        return schedule
    
    def ScheduleSimpleTrip(self, parameters):
        numberOfStops = parameters.NumberOfStops
        expectedTime = parameters.ExpectedTripTime
        batteryCapacity = parameters.BatteryCapacity
        hasCharge = parameters.HasDestinationCharger
        vehicle = parameters.Vehicle
        self.TripBuilder = SimpleTripBuilder(numberOfStops, hasCharge)
        tripName = parameters.TripName
        return self.ScheduleTrip(expectedTime, batteryCapacity, vehicle, SimpleEnvironment, tripName)

    def ScheduleFileTrip(self, parameters):
        routeFileName = parameters.RouteFileName
        chargersFileName = parameters.ChargerFileName
        expectedTime = parameters.ExpectedTripTime
        batteryCapacity = parameters.BatteryCapacity
        hasCharge = parameters.HasDestinationCharger
        vehicle = parameters.Vehicle
        tripName = parameters.TripName
        self.TripBuilder = FileTripBuilder(routeFileName, chargersFileName, hasCharge)
        return self.ScheduleTrip(expectedTime, batteryCapacity, vehicle, EvTripScheduleEnvironment,tripName)

    def ScheduleOsrmTrip(self, parameters):
        startPoint = parameters.StartPoint
        endPoint = parameters.EndPoint
        expectedTime = parameters.ExpectedTripTime
        batteryCapacity = parameters.BatteryCapacity
        hasCharge = parameters.HasDestinationCharger
        vehicle = parameters.Vehicle
        tripName = parameters.TripName
        self.TripBuilder = OsrmTripBuilder(startPoint, endPoint, hasCharge)
        return self.ScheduleTrip(expectedTime, batteryCapacity, vehicle, EvTripScheduleEnvironment,tripName)