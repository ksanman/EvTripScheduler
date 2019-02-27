class RoadSegment:
    def __init__(self, distance, duration, elevation):
        self.Distance = distance
        self.Duration = duration
        self.Speed = distance / duration
        self.Elevation = elevation