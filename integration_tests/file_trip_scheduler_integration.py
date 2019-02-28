from context import FileTripBuilder, Optimizer, EvTripScheduleEnvironment, NissanLeaf, Optimizer, Visualize

routeFilePath = "data/stgeorge_route.txt"
chargersFilePath = "data/stgeorge_chargers.txt"
expectedTime = 28
batteryCapacity = 40
hasCharge = True
vehicle = 'NissanLeaf'

tripBuilder = FileTripBuilder(routeFilePath, chargersFilePath, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle)

environment = EvTripScheduleEnvironment(trip)

optimizer = Optimizer()

expectedValues = optimizer.ComputeExpectedValue(environment)

policy = optimizer.GetOptimalPolicy(expectedValues, environment)

schedule = optimizer.GetSchedule(policy, trip.Route, environment)

schedule.Print()

# Add Visualizations here. 
visualizer = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
#visualizer.VisualizeRewards(*environment.GetRewards())
#visualizer.VisualizeValueTable(expectedValues)
#visualizer.VisualizePolicy(policy)
visualizer.DisplayEvaluationGraphs(schedule.TripStats, trip.Route.PossibleStops)
print 'Done'