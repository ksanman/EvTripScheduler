import folium
import os 

from ..trip_builder import Coordinate
from ..trip_builder import Osrm

class Schedule:
    def __init__(self, coordinates, chargingStops, finalStop, tripTime, finalBatteryLevel, isSuccesful, tripStats, timeBlockConstant, title):
        """ The resulting schedule of the trip. 

            Coordinates - coordinates that make up the route, from OSRM. 
            ChargingStops - A list of stops and how long to stop there. 
            TripTime - The total time the trip took. 
            FinalBatteryLevel - The final battery level. 
            IsSuccessful - If the trip was successful. 
            TripStats - Stats about each time step, tells us what the model was doing. This is for visualization. 
            Osrm = The osrm routing service. 
            TimeBlockConstant - The time precision. 
            Title - The title of the trip. 
        """
        self.Coordinates = coordinates
        self.ChargingStops = chargingStops
        self.TripTime = tripTime
        self.FinalBatteryLevel = finalBatteryLevel
        self.IsSuccesful = isSuccesful
        self.FinalStop = finalStop
        self.TripStats = tripStats
        self.Osrm = Osrm()
        self.TimeBlockConstant = timeBlockConstant
        self.Title = title

    def Print(self):
        if self.IsSuccesful:
            time = self.GetTime()
            print 'Trip {0} successful! \nTotal Time: {1} ({2} time blocks) \n'.format(self.Title, time, self.TripTime)
                
            if self.ChargingStops != []:
                print 'Stop at the following locations: \n\n'

            for order, stop in enumerate(self.ChargingStops):
                print '{0}: {1} (stop {2}) for {3} minutes ({4} time blocks)'\
                    .format(order + 1, stop.Name, stop.Order, stop.TimeAtStop*self.TimeBlockConstant, stop.TimeAtStop)

        else:
            print 'Trip failed after {0} minutes ({1} time blocks) at {2} (stop {3})'\
                .format(self.TripTime* self.TimeBlockConstant, self.TripTime, self.FinalStop.Name, self.FinalStop.Order)

        self.DrawMap()

    def GetTime(self):
        totalMinutes = self.TripTime* self.TimeBlockConstant
        days = totalMinutes/24/60
        hours = totalMinutes/60%24
        minutes = totalMinutes%60

        return '{0} days, {1} hours, {2} minutes'.format(days, hours, minutes) if days > 0 \
            else '{0} hours, {1} minutes'.format(hours, minutes) if hours > 0 \
                else '{0} minutes'.format(minutes)
        

    def DrawMap(self): 
        """
            Draw a route on an OSM map and display the charging points on top of it. 
        """

        if self.Coordinates != []:
            # Create the map and add the line
            print('Drawing route')

            routePoints = [Coordinate(self.Coordinates[0].Latitude, self.Coordinates[0].Longitude)]
            routePoints.extend([ stop.Location for stop in self.ChargingStops])
            routePoints.append(Coordinate(self.Coordinates[-1].Latitude, self.Coordinates[-1].Longitude))
            route = self.Osrm.GetRouteFromOsrm(routePoints)
            
            self.OsrmRoute = route['RawData']

            m = folium.Map(location=[41.9, -97.3], zoom_start=4)
            polyline = folium.PolyLine(locations=route['Coordinates'], weight=5)
            m.add_child(polyline)

            for stop in self.ChargingStops:
                folium.Marker(location=[stop.Location.Latitude, stop.Location.Longitude], popup=stop.Name + '\n\n Stop for {0} mintues'.format(stop.TimeAtStop*self.TimeBlockConstant)).add_to(m)


            if not os.path.exists("temp"):
                os.mkdir('temp/')

            filepath = 'temp/map.html'
            m.save(filepath)
            #webbrowser.open(filepath)

            print 'Saved route to {0}'.format(filepath)