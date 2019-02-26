class TripParamters:
    def __init__(self, startLocation, destination, expectedTravelTime, car, filenames=[], numberOfChargers=0, distances=[], hasChargerAtDestination=True):
        self.StartLocation = startLocation
        self.Destination = destination
        self.ExpectedTravelTime = expectedTravelTime
        self.Car = car
        self.NumberOfChargers = numberOfChargers
        self.Distances = distances
        self.Filenames = []
        self.HasChargerAtDestination = hasChargerAtDestination