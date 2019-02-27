from context import SimpleEnvironment, Trip
from visualize import Visualize

class EnvironmentVisualization:
    def run(self):
        
        trip = Trip(3, 3, 3, True)
        environment = SimpleEnvironment(trip)
        visualize = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
        drivingRewards, chargingRewards = environment.GetRewards()
        visualize.VisualizeRewards(drivingRewards, chargingRewards)

if __name__ == '__main__':
    visual = EnvironmentVisualization()
    visual.run()