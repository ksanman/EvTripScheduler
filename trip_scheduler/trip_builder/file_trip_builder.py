from trip_builder import TripBuilder
from charger_context import ChargerContext
from trip import Stop
from routing import Osrm
from trip import Coordinate
from trip import RoadSegment
from trip import ChargerConnection
from routing import Route
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
        route = [Stop(0, "Start", 0, 0, 0, ChargerConnection(0,0), Coordinate(startLocation[0], startLocation[1]))]

        if self.HasDestinationCharger:
            for stop in range(len(self.Chargers)):
                charger = self.Chargers[stop]
                chargerLocation = Coordinate(charger.AddressInfo.Latitude, charger.AddressInfo.Longitude)
                cost = charger.UsageCost if charger.UsageCost is not None else 0
                chargerConnection = ChargerConnection(cost, charger.Connections[0].PowerKw, charger.Connections[0].Amps, charger.Connections[0].Voltage)
                distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints(route[stop].Location, chargerLocation)
                energyExpended = RoundUp(self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0)))
                route.append(Stop(stop, str(charger.AddressInfo.Title) ,energyExpended, distanceFromPrevious, self.ConvertFromSecondsToFifteenMinuteBlock(durationFromPrevious), chargerConnection, chargerLocation))

        else:
            for stop in range(len(self.Chargers)-1):
                charger = self.Chargers[stop]
                chargerLocation = Coordinate(charger.AddressInfo.Latitude, charger.AddressInfo.Longitude)
                cost = charger.UsageCost if charger.UsageCost is not None else 0
                chargerConnection = ChargerConnection(cost, charger.Connections[0].PowerKw, charger.Connections[0].Amps, charger.Connections[0].Voltage)
                distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints(route[stop].Location, chargerLocation)
                energyExpended = RoundUp(self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0)))
                route.append(Stop(stop, str(charger.AddressInfo.Title), energyExpended, distanceFromPrevious,  self.ConvertFromSecondsToFifteenMinuteBlock(durationFromPrevious), chargerConnection, chargerLocation))

            destinationLocation =osrmRoute['Coordinates'][-1]
            destinationCoordinate = Coordinate(destinationLocation[0], destinationLocation[1])
            distanceFromPrevious, durationFromPrevious = self.Osrm.GetDistanceAndDurationBetweenPoints(route[-1].Location, destinationCoordinate)
            energyExpended = self.Vehicle.Drive(RoadSegment(distanceFromPrevious, durationFromPrevious, 0))
            route.append(Stop(self.NumberOfStops-1, "Destination", energyExpended, destinationCoordinate,  self.ConvertFromSecondsToFifteenMinuteBlock(durationFromPrevious), location=destinationCoordinate))

        return Route(route, osrmRoute['Polyline'], osrmRoute['Coordinates'])