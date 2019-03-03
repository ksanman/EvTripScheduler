from context import TripParameters, TripScheduler

parameters = TripParameters(expectedTripTime=10, batteryCapacity=8, vehicle='SimpleVehicle', numberOfStops=10, hasDestinationCharger=True)

scheduler = TripScheduler()
schedule = scheduler.Schedule(parameters)
schedule.Print()