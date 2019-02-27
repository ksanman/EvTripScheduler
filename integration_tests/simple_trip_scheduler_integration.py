from context import SimpleTripBuilder, Optimizer, SimpleEnvironment, Vehicle, Optimizer

numberOfStops = 17
expectedTime = 28
batteryCapacity = 4
hasCharge = True

tripBuilder = SimpleTripBuilder(numberOfStops, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, Vehicle(batteryCapacity))

environment = SimpleEnvironment(trip)

optimizer = Optimizer()

expectedValues = optimizer.ComputeExpectedValue(environment)

policy = optimizer.GetOptimalPolicy(expectedValues, environment)

print 'Done'

#schedule = optimizer.GetSchedule(policy, environment)