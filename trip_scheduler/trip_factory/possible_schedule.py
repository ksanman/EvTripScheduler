class PossibleSchedule:
    def __init__(self, polyline, coordinates, expectedTripTime, car, possibleStops):
        self.Polyline = polyline
        self.Coordinates = coordinates
        self.ExpectedTripTime = expectedTripTime
        self.Car = car
        self.PossibleStops = possibleStops