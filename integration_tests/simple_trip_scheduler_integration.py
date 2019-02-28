from context import SimpleTripBuilder, Optimizer, SimpleEnvironment, Vehicle, Optimizer

numberOfStops = 10
expectedTime = 25
batteryCapacity = 5
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

print 'Done'

#schedule = optimizer.GetSchedule(policy, environment)