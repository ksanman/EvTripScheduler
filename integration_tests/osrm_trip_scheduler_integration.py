from context import OsrmTripBuilder, Optimizer, EvTripScheduleEnvironment, Optimizer, Visualize

startPoint=['41.740256','-111.841764']
endPoint=['37.095169','-113.575974']
expectedTime = 28
batteryCapacity = 40
hasCharge = True
vehicle = 'NissanLeaf'

tripBuilder = OsrmTripBuilder(startPoint, endPoint, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle)

environment = EvTripScheduleEnvironment(trip)

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