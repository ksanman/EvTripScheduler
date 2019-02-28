from trip_builder import TripBuilder
from charger_context import ChargerContext
from stop import Stop
from osrm import Osrm
from coordinate import Coordinate
from road_segment import RoadSegment
from charger_connection import ChargerConnection
from route import Route
from ..utility import RoundUp

class FileTripBuilder(TripBuilder, object):
    def __init__(self, routeFilePath, chargersFilePath, hasDestinationCharger=None):
        self.RouteFilePath = routeFilePath
        self.ChargersFilePath = chargersFilePath
        self.HasDestinationCharger = hasDestinationCharger
        self.ChargerContext = ChargerContext()
        self.Osrm = Osrm()
        super(FileTripBuilder, self).__init__()

    def GetNumberOfStops(self):
        self.Chargers = self.ChargerContext.GetChargersFromFile(self.ChargersFilePath)
        self.NumberOfStops = len(self.Chargers) + 2 if self.HasDestinationCharger != None and self.HasDestinationCharger is False else len(self.Chargers) + 1
        return self.NumberOfStops

    def GetHasDestinationCharger(self):
        return self.HasDestinationCharger

    def GetRoute(self):
        osrmRoute = self.Osrm.GetRouteFromFile(self.RouteFilePath)
        startLocation = osrmRoute['Coordinates'][0]
        route = [Stop(0, "Start", 0, 0, 0, location=Coordinate(startLocation[0], startLocation[1]))]

        if self.HasDestinationCharger:
            for stop in range(len(self.Chargers)):
                charger = self.Chargers[stop]
                chargerLocation = Coordinate(charger.AddressInfo.Latitude, charger.AddressInfo.Longitude)
                chargerConnection = ChargerConnection(charger.UsageCost, charger.Connections[0].PowerKw, charger.Connections[0].Amps, charger.Connections[0].Voltage)
                distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints(route[stop].Location, chargerLocation)
                energyExpended = RoundUp(self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0)))
                route.append(Stop(stop, charger.AddressInfo.Title,energyExpended, distanceFromPrevious, RoundUp(durationFromPrevious), chargerConnection, chargerLocation))

        else:
            for stop in range(len(self.Chargers)-1):
                charger = self.Chargers[stop]
                chargerLocation = Coordinate(charger.AddressInfo.Latitude, charger.AddressInfo.Longitude)
                chargerConnection = ChargerConnection(charger.UsageCost, charger.Connections[0].PowerKw, charger.Connections[0].Amps, charger.Connections[0].Voltage)
                distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints(route[stop].Location, chargerLocation)
                energyExpended = RoundUp(self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0)))
                route.append(Stop(stop, charger.AddressInfo.Title,energyExpended, distanceFromPrevious,  RoundUp(durationFromPrevious), chargerConnection, chargerLocation))

            destinationLocation =osrmRoute['Coordinates'][-1]
            destinationCoordinate = Coordinate(destinationLocation[0], destinationLocation[1])
            distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints(route[-1].Location, destinationCoordinate)
            energyExpended = self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0))
            route.append(Stop(self.NumberOfStops-1, "Destination", energyExpended, destinationCoordinate,  RoundUp(durationFromPrevious), location=destinationCoordinate))

        return Route(route, osrmRoute['Polyline'], osrmRoute['Coordinates'])