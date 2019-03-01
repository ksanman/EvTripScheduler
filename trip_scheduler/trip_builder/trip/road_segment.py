class RoadSegment:
    def __init__(self, distance, duration, elevation):
        self.Distance = distance
        self.Duration = duration
        self.Speed = distance / ((duration / 60) / 60)
        self.Elevation = elevation