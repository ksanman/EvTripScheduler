class RoadSegment:
    def __init__(self, distance, duration, elevation):
        self.Distance = float(distance)
        self.Duration = float(duration)
        self.Speed = float(distance) / ((float(duration) / 60.0) / 60.0)
        self.Elevation = elevation