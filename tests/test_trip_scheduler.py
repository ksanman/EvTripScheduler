import unittest

from context import TripParameters, Location , Charger, Address, Connection, SimpleCar

class Test_TripScheduler(unittest.TestCase):
    def test_parameter_initialization(self):
        startPoint = Location("Start", Address(0, 0, 0))
        destination = Location("Destination", Address(3, 3, 3))
        expectedTravelTime = 3
        car = SimpleCar(3)

        tripParameters = TripParameters(startPoint, destination, expectedTravelTime, car)

        trips = TripFactory.BuildPossibleSchedulesForTrips([tripParameters])

        optimizedSchedules = Optimizer.OptimizerTripSchedules(trips)

if __name__ == '__main__':
    unittest.main(exit=False)