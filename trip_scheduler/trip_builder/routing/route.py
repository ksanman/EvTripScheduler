class Route:
    def __init__(self, possibleStops, polyline='', coordinates = []):
        self.Polyline = polyline
        self.Coordinates = coordinates
        self.PossibleStops = possibleStops