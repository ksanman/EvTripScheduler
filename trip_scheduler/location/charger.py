from location import Location

class Charger(location):
    def __init__(self, id, title, address, connections, usageCost nearestIntersection):
        self.ID = id
        self.Title = title
        self.Address = address
        self.Connections = connections
        self.UsageCost = usageCost
        self.NearestIntersection = nearestIntersection