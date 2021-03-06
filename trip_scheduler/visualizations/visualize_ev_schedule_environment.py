from ..environment import EvTripScheduleEnvironment
from..trip_builder import Trip, Stop, ChargerConnection, SimpleVehicle, Route
from visualize import Visualize

class EvTripScheduleEnvironmentVisualization:
    def run(self):
        # Build a simple trip of 3 locations, an expected time of 3, and a battery capacity of 3. 
        stops = [Stop(1, "Start", 0, 0, 0, ChargerConnection(0.13, power=25)), Stop(2, "2", 1, 1, 1, ChargerConnection(0.13, power=25)), Stop(3, "End", 1, 1, 1, ChargerConnection(0.13, power=25))]
        possibleStops = Route(stops)
        expectedTime = 3
        vehicle = SimpleVehicle(3)
        trip = Trip(expectedTripTime=expectedTime, route=possibleStops, vehicle=vehicle)
        environment = EvTripScheduleEnvironment(trip)
        visualize = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
        drivingRewards, chargingRewards = environment.GetRewards()
        visualize.VisualizeRewards(drivingRewards, chargingRewards)

if __name__ == '__main__':

    visual = EvTripScheduleEnvironmentVisualization()
    visual.run()