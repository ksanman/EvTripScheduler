from context import TripParameters, TripScheduler

parameters = TripParameters(expectedTripTime=28, batteryCapacity=40, vehicle='NissanLeaf', routeFileName='data/stgeorge_route.txt', chargersFileName='data/stgeorge_chargers.txt', hasDestinationCharger=True)
scheduler = TripScheduler()
schedule = scheduler.Schedule(parameters)
schedule.Print()