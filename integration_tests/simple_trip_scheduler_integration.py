from context import SimpleTripBuilder, Optimizer, SimpleEnvironment, Vehicle, Optimizer, Visualize

numberOfStops = 10
expectedTime = 12
batteryCapacity = 8
hasCharge = True

tripBuilder = SimpleTripBuilder(numberOfStops, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, Vehicle(batteryCapacity))

environment = SimpleEnvironment(trip)

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