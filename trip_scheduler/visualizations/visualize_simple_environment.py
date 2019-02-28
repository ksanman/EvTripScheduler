from ..environment import SimpleEnvironment
from ..trip_builder import Trip
from visualize import Visualize

class SimpleEnvironmentVisualization:
    def run(self):
        
        trip = Trip(3, 3, 3, True)
        environment = SimpleEnvironment(trip)
        visualize = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
        drivingRewards, chargingRewards = environment.GetRewards()
        visualize.VisualizeRewards(drivingRewards, chargingRewards)

if __name__ == '__main__':
    visual = SimpleEnvironmentVisualization()
    visual.run()