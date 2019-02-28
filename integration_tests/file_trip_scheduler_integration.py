from context import FileTripBuilder, Optimizer, EvTripScheduleEnvironment, NissanLeaf, Optimizer, Visualize
from time import time

routeFilePath = "data/stgeorge_route.txt"
chargersFilePath = "data/stgeorge_chargers.txt"
expectedTime = 28
batteryCapacity = 40
hasCharge = True
vehicle = 'NissanLeaf'

totalStartTime = time()

# Build the route
startTripTime = time()

tripBuilder = FileTripBuilder(routeFilePath, chargersFilePath, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle)

endTripTime = time()

print 'Trip built in {0} seconds'.format(endTripTime - startTripTime)

# Get the optimial schedule

startOptimalScheduleTime = time()
# Construct the environment. 

startEnvTime = time()

environment = EvTripScheduleEnvironment(trip)

endEnvTime = time()

print 'Environment constructed in {0} seconds'.format(endEnvTime - startEnvTime)

# Optimize the Schedule.  

startOptimizeTime = time()
optimizer = Optimizer()

# Expected Value

startExpectedValueTime = time()
expectedValues = optimizer.ComputeExpectedValue(environment)

endExpectedValueTime = time()

print 'Expected value found in {0} seconds'.format(endExpectedValueTime - startExpectedValueTime)

# Policy
startPolicyTime = time()
policy = optimizer.GetOptimalPolicy(expectedValues, environment)
endPolicyTime = time()

print 'Optimal Policy found in {0} seconds'.format(endPolicyTime - startPolicyTime)

# Solve
startScheduleTime = time()
schedule = optimizer.GetSchedule(policy, trip.Route, environment)
endScheduleTime = time()

print 'Schedule found in {0} seconds'.format(endScheduleTime - startScheduleTime)

endOptimalScheduleTime = time()

print 'Optimization done in {0} seconds'.format(endOptimalScheduleTime - startOptimalScheduleTime)

totalEndTime = time() 

print 'Optimal trip found in {0} seconds'.format(totalStartTime - totalEndTime)

schedule.Print()

# Add Visualizations here. 
visualizer = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
visualizer.VisualizeRewards(*environment.GetRewards())
#visualizer.VisualizeValueTable(expectedValues)
#visualizer.VisualizePolicy(policy)
visualizer.DisplayEvaluationGraphs(schedule.TripStats, trip.Route.PossibleStops)
print 'Done'