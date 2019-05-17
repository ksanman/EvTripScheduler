from trip_builder import TripBuilder
from charger_context import ChargerContext
from trip import Stop
from routing import Osrm
from trip import Coordinate
from trip import RoadSegment
from trip import ChargerConnection
from routing import Route
from ..utility import RoundUp
from math import radians, cos, sin, asin, sqrt
from trip_scheduler.trip_builder.vehicle.energy_model import EnergyConsumptionModel

class OsrmTripBuilder(TripBuilder, object):
    def __init__(self, startPoint, endPoint, hasDestinationCharger=None):
        self.StartPoint = startPoint
        self.EndPoint = endPoint
        self.HasDestinationCharger = hasDestinationCharger
        self.ChargerContext = ChargerContext()
        self.Osrm = Osrm()
        self.EnergyModel = EnergyConsumptionModel()
        super(OsrmTripBuilder, self).__init__()

    def GetNumberOfStops(self):
        self.OsrmRoute = self.Osrm.GetRouteFromOsrm([Coordinate(self.StartPoint[0], self.StartPoint[1]), Coordinate(self.EndPoint[0], self.EndPoint[1])])
        self.Chargers = self.ChargerContext.GetNearestChargersFromDatabase(self.OsrmRoute['Coordinates'], 3)
        self.NumberOfStops = len(self.Chargers) + 2 if self.HasDestinationCharger != None and self.HasDestinationCharger is False else len(self.Chargers) + 1
        return self.NumberOfStops

    def GetHasDestinationCharger(self):
        return self.HasDestinationCharger

    def GetRoute(self):
        osrmRoute = self.OsrmRoute
        startLocation = self.StartPoint
        nearestPoint = self.GetNearestPoint(Coordinate(float(startLocation[0]), float(startLocation[1]), 0))
        route = [Stop(0, "Start", 0, 0, 0, ChargerConnection(0,0), Coordinate(float(nearestPoint[0]), float(nearestPoint[1]), self.Osrm.GetElevation(startLocation[0], startLocation[1])), Coordinate(nearestPoint[0], nearestPoint[1], 0))]

        if self.HasDestinationCharger:
            stop = 0
            for stop in range(len(self.Chargers)):
                charger = self.Chargers[stop]
                nearestPoint = self.GetNearestPoint(Coordinate(charger.IntersectionLatitude, charger.IntersectionLongitude, 0))
                chargerLocation = Coordinate(charger.AddressInfo.Latitude, charger.AddressInfo.Longitude, 0)
                intersection = Coordinate(charger.IntersectionLatitude, charger.IntersectionLongitude, 0)
                cost = charger.UsageCost if charger.UsageCost is not None else 0
                chargerConnection = ChargerConnection(cost, charger.Connections[0].PowerKw, charger.Connections[0].Amps, charger.Connections[0].Voltage)
                distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints([route[stop-1].Location, intersection])
                energyExpended = RoundUp(self.CalculateEnergyExpended(route[stop-1].Intersection, Coordinate(nearestPoint[0], nearestPoint[1], 0)))    
                route.append(Stop(stop + 1, str(charger.AddressInfo.Title) ,energyExpended, distanceFromPrevious[0], self.ConvertToTimeBlock(durationFromPrevious[0]), chargerConnection, chargerLocation, intersection))

        else:
            for stop in range(len(self.Chargers)):
                charger = self.Chargers[stop]
                nearestPoint = self.GetNearestPoint(Coordinate(charger.IntersectionLatitude, charger.IntersectionLongitude, 0))
                chargerLocation = Coordinate(charger.AddressInfo.Latitude, charger.AddressInfo.Longitude, 0)
                intersection = Coordinate(charger.IntersectionLatitude, charger.IntersectionLongitude, 0)
                cost = charger.UsageCost if charger.UsageCost is not None else 0
                chargerConnection = ChargerConnection(cost, charger.Connections[0].PowerKw, charger.Connections[0].Amps, charger.Connections[0].Voltage)
                distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints([route[stop-1].Location, chargerLocation])
                energyExpended = RoundUp(self.CalculateEnergyExpended(route[stop-1].Intersection, Coordinate(nearestPoint[0], nearestPoint[1], 0)))
                route.append(Stop(stop + 1, str(charger.AddressInfo.Title), energyExpended, distanceFromPrevious[0],  self.ConvertToTimeBlock(durationFromPrevious[0]), chargerConnection, chargerLocation, intersection))

            destinationLocation = self.EndPoint
            destinationCoordinate = Coordinate(float(destinationLocation[0]), float(destinationLocation[1]), 0)
            distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints([route[-1].Location, destinationCoordinate])
            energyExpended = RoundUp(self.CalculateEnergyExpended(route[len(self.Chargers)].Intersection, destinationCoordinate))
            route.append(Stop(self.NumberOfStops, "Destination", energyExpended, distanceFromPrevious[0],  self.ConvertToTimeBlock(durationFromPrevious[0]), location=destinationCoordinate))

        return Route(route, osrmRoute['Polyline'], osrmRoute["Elevations"])


    def CalculateEnergyExpended(self, previousLocation, currentLocation):
        elevations = self.OsrmRoute["Elevations"]
        startIndex = self.GetIndex(previousLocation)
        endIndex = self.GetIndex(currentLocation)

        if startIndex == -1:
           startPointLat, startPointLong = self.GetNearestPoint(previousLocation) 
           startIndex = self.GetIndex(Coordinate(startPointLat, startPointLong, 0))
        if endIndex == -1:
            endPointLat, endPointLong = self.GetNearestPoint(currentLocation) 
            endIndex = self.GetIndex(Coordinate(endPointLat, endPointLong, 0))

        energy = 0
        segments = elevations[startIndex:endIndex]
        distances, durations = self.Osrm.GetDistanceAndDurationBetweenPoints(segments)

        for i, coordinate in enumerate(segments):
            if i-1 < 0:
                continue

            elevationDelta = coordinate.Elevation - segments[i-1].Elevation
            distanceKms, durationSecs = distances[i-1], durations[i-1]
            speed = float(distanceKms * 1000) / float(durationSecs) #m/s

            if i - 2 > 0:
                distancePrev = distances[i-2]
                durationPrev= durations[i-2]
                speedPrev = float(distancePrev * 1000) / float(durationPrev) #m\s
                acceleration = (speed - speedPrev)/(durationSecs + durationPrev)
            else:
                acceleration = 0

            grade = elevationDelta / (distanceKms * 1000)
            #energy += self.EnergyModel.ComputerEnergyExpended(self.Vehicle, acceleration, speed, grade, durationSecs, distanceKms)
            energy += self.Vehicle.Drive(RoadSegment(distanceKms, durationSecs, elevationDelta))
    
        return energy


    def GetElevationChange(self, startCoordinate, endCoordinate):
        elevations = self.OsrmRoute["Elevations"]
        startIndex = self.GetIndex(startCoordinate)
        endIndex = self.GetIndex(endCoordinate)

        if startIndex == -1 or endIndex == -1:
            return 0

        elevationDelta = 0

        for i, coordinate in enumerate(elevations[startIndex:endIndex]):
            if i-1 >= 0 and elevations[i-1] != None and coordinate.Elevation > elevations[i-1].Elevation:
                elevationDelta += coordinate.Elevation - elevations[i-1].Elevation

        return elevationDelta

    def GetIndex(self, coordinate):
        elevations = self.OsrmRoute["Elevations"]

        for i, coord in enumerate(elevations):
            if coord.Latitude == coordinate.Latitude and coord.Longitude == coordinate.Longitude:
                return i
        return -1

    def GetNearestPoint(self, coordinate):
        distances = []
        distanceList = []
        for coord in self.OsrmRoute["Elevations"]:
            distance = self.Haversine(coordinate.Longitude, coordinate.Latitude, coord.Longitude, coord.Latitude)
            distanceList.append(distance)
            distances.append({ "Distance":distance, "Latitude":coord.Latitude, "Longitude":coord.Longitude})

        shortest = min(distanceList)

        for distance in distances:
            if distance["Distance"] == shortest:
                return distance["Latitude"], distance["Longitude"]

        return coordinate.Latitude, coordinate.Longitude


    def Haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    

