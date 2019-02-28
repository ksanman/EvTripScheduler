from ..environment import SimpleEnvironment
from ..trip_builder import Trip
from ..optimizer import Optimizer
from visualize import Visualize

class OptimizerVisualization:
    def run(self):
        trip = Trip(10, 10, 5, True)
        environment = SimpleEnvironment(trip)
        visualize = Visualize(environment.NumberOfStops, environment.MaxTripTime, environment.MaxBattery, environment.ExpectedTripTime)
        optimizer = Optimizer()
        values = optimizer.ComputeExpectedValue(environment)
        policy = optimizer.GetOptimalPolicy(values, environment)
        visualize.VisualizeValueTable(values)
        visualize.VisualizePolicy(policy)

if __name__ == '__main__':
    visual = OptimizerVisualization()
    visual.run()