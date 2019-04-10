import json
import polyline
import requests
from ..trip import Coordinate
from ...utility import RoundUp

class Osrm:
    def __init__(self):
        #self.RouteRequestString = 'http://router.project-osrm.org/route/v1/driving/{0}?overview=full&steps=true'
        self.RouteRequestString = 'http://localhost:5001/route/v1/driving/{0}?overview=full&steps=true'
        #self.DistanceRequestString = 'http://router.project-osrm.org/route/v1/driving/{0},{1};{2},{3}?overview=simplified'  
        self.DistanceRequestString = 'http://localhost:5001/route/v1/driving/{0},{1};{2},{3}?overview=simplified'  
        #self.ElevationRequestString = 'https://api.open-elevation.com/api/v1/lookup?locations={0},{1}'
        self.ElevationRequestString = 'http://192.168.99.100:8080/api/v1/lookup?locations={0},{1}'

    def GetRouteFromOsrm(self, coordinates):
        """ Submits a request to OSRM to get a route data. All that are needed are the start coordinates
            and the end coordinates in latitude, longitude pairs. 
        """

        print 'Getting route...'
        urlRequest = self.GetFullRequestString(coordinates)
        response = requests.get(urlRequest)
        content = response.content 
        jsonData = content.decode('utf8').replace("'", '"')
        print 'Route recieved.'
        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(jsonData)
        return self.GetRouteFromJson(data)

    def GetFullRequestString(self, coordinates):

        coordinateString = ''

        for coordinate in coordinates:
            coordinateString += '{0},{1};'.format(coordinate.Longitude, coordinate.Latitude)

        coordinateString = coordinateString[:-1]

        return self.RouteRequestString.format(coordinateString)
            
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
        return {'RawData': data, 'Polyline': route['geometry'], 'Coordinates':polyline.decode(route['geometry']), 'Intersections': intersections}

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

    def GetElevation(self, latitude, longitude):
        try:
            request = self.ElevationRequestString.format(latitude, longitude)
            r = requests.get(request)
            c = r.content
            my_json = c.decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            results = data['results']
            elevationData = results[0]['elevation']
            elevation = float(elevationData)
            return elevation
        except Exception as e:
            print e
            return 0

    def GetElevationFromCoordinates(self, coordinates):
        requestString = 'http://192.168.99.100:8080/api/v1/lookup'

        headers = {
            'Accept':'application/json',
            'Content-Type':'application/json'
        }
        elevations = []
        chunks = [coordinates[x:x+1000] for x in xrange(0, len(coordinates), 1000)]
        for chunk in chunks:
            locations = [{"latitude":coordinate[0], "longitude":coordinate[1]} for coordinate in chunk]

            data = {"locations":locations}

            jsonData = json.dumps(data)
            r = requests.post(requestString, data=jsonData, headers=headers)
            c = r.content
            my_json = c.decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            results = data['results']
            for result in results:
                elevationData = result['elevation']
                latitudeData = result['latitude']
                longitudeData = result['longitude']
                elevations.append(Coordinate(float(latitudeData), float(longitudeData), float(elevationData)))
        return elevations