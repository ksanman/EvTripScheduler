from context import OsrmTripBuilder, Optimizer, EvTripScheduleEnvironment, Optimizer, Visualize

title = 'Energy Estimation'
startPoint=['41.7457','-111.83395']
endPoint=['41.21069','-112.01111']
expectedTime = 120
batteryCapacity = 24
hasCharge = False
vehicle = 'NissanLeaf'
timeBlockConstant = 5

tripBuilder = OsrmTripBuilder(startPoint, endPoint, hasCharge)

trip = tripBuilder.BuildTrip(expectedTime, batteryCapacity, vehicle, timeBlockConstant, title)

totalEnergy = 0
for stop in trip.Route.PossibleStops:
    totalEnergy += stop.EnergyExpended

print totalEnergy