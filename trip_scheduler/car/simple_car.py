from car import Car
from battery import SimpleBattery

class SimpleCar(Car):
    def __init__(self, batteryCapacity):
        super(SimpleCar, self).__init__(SimpleBattery(batteryCapacity))