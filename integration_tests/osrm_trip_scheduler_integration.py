from context import OsrmTripBuilder, Optimizer, EvTripScheduleEnvironment, Optimizer, Visualize
from time import time

#title = 'Logan to St George'
title = 'Logan to Salt Lake'
startPoint=['41.740256','-111.841764']
#endPoint=['37.095169','-113.575974'] #st george
#endPoint = ['38.573315', '-109.549843'] #moab
endPoint = [40.758701, -111.876183]
expectedTime = 120
batteryCapacity = 24
hasCharge = True
vehicle = 'NissanLeaf'
timeBlockConstant = 5

totalTripStart = time()

buildStart = time()

tripBuilder = OsrmTripBuilder(startPoint, endPoint, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle, timeBlockConstant, title)

print '\nTrip built in {0} seconds \n'.format(time() - totalTripStart)

startOptimalScheduleTime = time()
startEnvTime = time()

environment = EvTripScheduleEnvironment(trip)

print 'Environment constructed in {0} seconds \n'.format(time() - startEnvTime)

startOptimizeTime = time()

optimizer = Optimizer(timeBlockConstant)


startExpectedValueTime = time()
expectedValues = optimizer.ComputeExpectedValue(environment)

print 'Expected value found in {0} seconds \n'.format(time() - startExpectedValueTime)

startPolicyTime = time()
policy = optimizer.GetOptimalPolicy(expectedValues, environment)
print 'Optimal Policy found in {0} seconds \n'.format(time() - startPolicyTime)

startScheduleTime = time()
schedule = optimizer.GetSchedule(policy, trip, environment)

print 'Schedule found in {0} seconds \n'.format(time() - startScheduleTime)

print 'Optimization done in {0} seconds \n'.format(time() - startOptimalScheduleTime)

print 'Optimal trip found in {0} seconds \n'.format(time() - totalTripStart)

schedule.Print()

# Add Visualizations here. 
visualizer = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
visualizer.VisualizeRewards(*environment.GetRewards())
visualizer.VisualizeValueTable(expectedValues)
visualizer.VisualizePolicy(policy)
visualizer.DisplayEvaluationGraphs(schedule.TripStats, trip.Route.PossibleStops, trip.TripName)
print 'Done'