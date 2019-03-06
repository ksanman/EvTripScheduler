from context import DistanceTripBuilder, Optimizer, EvTripScheduleEnvironment, NissanLeaf, Optimizer, Visualize
from time import time

routeFilePath = "data/stgeorge_route.txt"
chargersFilePath = "data/stgeorge_chargers.txt"
expectedTime = 60
batteryCapacity = 24
hasCharge = True
vehicle = 'NissanLeaf'
timeBlockConstant = 2

#Logan to SLC
distancesAndTimes = [
    [12.8748,840],
    [51.499,2220],
    [17.7028,960],
    [41.8429,1860],
    [16.0,960],
    [3.2,540],
    [3.2,180]
]

# distancesAndTimes = [
#     [12.8748,840],
#     [51.499,2220],
#     [23.7028,960]
# ]

totalStartTime = time()

# Build the route
startTripTime = time()

tripBuilder = DistanceTripBuilder(distancesAndTimes, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle, timeBlockConstant)

endTripTime = time()

print '\nTrip built in {0} seconds \n'.format(endTripTime - startTripTime)

# Get the optimial schedule

startOptimalScheduleTime = time()
# Construct the environment. 

startEnvTime = time()

environment = EvTripScheduleEnvironment(trip)

endEnvTime = time()

print 'Environment constructed in {0} seconds \n'.format(endEnvTime - startEnvTime)

# Optimize the Schedule.  

startOptimizeTime = time()
optimizer = Optimizer(timeBlockConstant)

# Expected Value

startExpectedValueTime = time()
expectedValues = optimizer.ComputeExpectedValue(environment)

endExpectedValueTime = time()

print 'Expected value found in {0} seconds \n'.format(endExpectedValueTime - startExpectedValueTime)

# Policy
startPolicyTime = time()
policy = optimizer.GetOptimalPolicy(expectedValues, environment)
endPolicyTime = time()

print 'Optimal Policy found in {0} seconds \n'.format(endPolicyTime - startPolicyTime)

# Solve
startScheduleTime = time()
schedule = optimizer.GetSchedule(policy, trip.Route, environment)
endScheduleTime = time()

print 'Schedule found in {0} seconds \n'.format(endScheduleTime - startScheduleTime)

endOptimalScheduleTime = time()

print 'Optimization done in {0} seconds \n'.format(endOptimalScheduleTime - startOptimalScheduleTime)

totalEndTime = time() 

print 'Optimal trip found in {0} seconds \n'.format(totalEndTime - totalStartTime)

schedule.Print()

# Add Visualizations here. 
visualizer = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
visualizer.VisualizeRewards(*environment.GetRewards())
visualizer.VisualizeValueTable(expectedValues)
visualizer.VisualizePolicy(policy)
visualizer.DisplayEvaluationGraphs(schedule.TripStats, trip.Route.PossibleStops)
print 'Done'