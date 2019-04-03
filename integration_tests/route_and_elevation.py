from context import Osrm, Coordinate
from time import time

startPoint=['41.740256','-111.841764'] #Logan
endPoint = ['38.573315', '-109.549843'] #Moab

osrm = Osrm()

coordinates = [Coordinate(startPoint[0], startPoint[1]), Coordinate(endPoint[0], endPoint[1])]

route = osrm.GetRouteFromOsrm(coordinates)
startTime = time()
elevation = osrm.GetElevationFromCoordinates(route['Coordinates'])
print "Time to get elevation data for {0} coordinates: {1}".format(len(route["Coordinates"]), time()-startTime)

