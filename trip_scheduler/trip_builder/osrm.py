import json
import polyline
import requests
from coordinate import Coordinate
from ..utility import RoundUp

class Osrm:
    def __init__(self):
        self.RouteRequestString = 'http://router.project-osrm.org/route/v1/driving/{0},{1};{2},{3}?overview=full&steps=true'
        self.DistanceRequestString = 'http://router.project-osrm.org/route/v1/driving/{0},{1};{2},{3}?overview=simplified'  

    def GetRouteFromOsrm(self, start, end):
            """ Submits a request to OSRM to get a route data. All that are needed are the start coordinates
                and the end coordinates in latitude, longitude pairs. 
            """

            print 'Getting route...'
            urlRequest = self.RouteRequestString.format(start.AddressInfo.Longitude, start.AddressInfo.Latitude, end.AddressInfo.Longitude, end.AddressInfo.Latitude)
            response = requests.get(urlRequest)
            content = response.content 
            jsonData = content.decode('utf8').replace("'", '"')
            print 'Route recieved.'
            # Load the JSON to a Python list & dump it back out as formatted JSON
            data = json.loads(jsonData)
            return self.GetRouteFromJson(data)
            
    def GetRouteFromFile(self, filename):
        """ Loads a .json file containing a OSRM route response and constructs a route from the data. 
        """
        with open(filename, 'r') as file:
            content = file.read()

        jsonData = content.decode('utf8').replace("'", '"')
        data = json.loads(jsonData)
        return self.GetRouteFromJson(data)

    def GetRouteFromJson(self, data):
        """
        Build a route from json data. 
        Returns the route coordinates as well as all intersections along the route. 
        """
        route = data["routes"][0]
        print 'Building Route'
        #get the intersections along the route
        intersections = self.GetIntersections(route)
        return {'Polyline': route['geometry'], 'Coordinates':polyline.decode(route['geometry']), 'Intersections': intersections}

    def GetIntersections(self, data):
        """
        Get all the intersections along the route.
        """
        intersections = []
        for l in data['legs']:
            for s in l['steps']:
                for i in s['intersections']:
                    location = i['location']
                    intersections.append(Coordinate(location[1], location[0]))

        return intersections

    def GetDistanceAndDurationBetweenPoints(self, point1, point2):
        """ Get the distance and travel time between two lat/long points by traveling on a road. 
            Distance is returned in km, 
            Time is returned in seconds
        """
        request = self.DistanceRequestString.format(point1.Longitude, point1.Latitude, point2.Longitude, point2.Latitude)
        r = requests.get(request)
        c = r.content 
        my_json = c.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        route = data["routes"][0]
        distance = float(route["distance"]) / 1000
        duration = float(route['duration'])
        return distance, duration