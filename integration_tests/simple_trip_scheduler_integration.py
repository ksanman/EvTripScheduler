from context import SimpleTripBuilder, Optimizer, SimpleEnvironment, Optimizer, Visualize

numberOfStops = 3
expectedTime = 4
batteryCapacity = 2
hasCharge = True
vehicle = 'SimpleVehicle'

tripBuilder = SimpleTripBuilder(numberOfStops, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle)

environment = SimpleEnvironment(trip)

optimizer = Optimizer()

expectedValues = optimizer.ComputeExpectedValue(environment)

policy = optimizer.GetOptimalPolicy(expectedValues, environment)

schedule = optimizer.GetSchedule(policy, trip.Route, environment)

schedule.Print()

# Add Visualizations here. 
visualizer = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
visualizer.VisualizeRewards(*environment.GetRewards())
visualizer.VisualizeValueTable(expectedValues)
visualizer.VisualizePolicy(policy)
visualizer.DisplayEvaluationGraphs(schedule.TripStats, trip.Route.PossibleStops)
print 'Done'