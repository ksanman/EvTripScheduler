import unittest
from context import NissanLeaf

class Test_NissanLeaf(unittest.TestCase):
    def setUp(self):
        self.Car = NissanLeaf(30)

    def test_charge(self):
        batteryLevel = 0
        newLevel = 38
        test = self.Car.Charge(batteryLevel)
        self.assertEqual(test, newLevel)

        batteryLevel = 10
        newLevel = 48
        test = self.Car.Charge(batteryLevel)
        self.assertEqual(test, newLevel)

        batteryLevel = 50
        newLevel = 91
        test = self.Car.Charge(batteryLevel)
        self.assertEqual(test, newLevel)

        batteryLevel = 93.5
        newLevel = 100
        test = self.Car.Charge(batteryLevel)
        self.assertEqual(test, newLevel)

if __name__ == '__main__':
    unittest.main(exit=False)