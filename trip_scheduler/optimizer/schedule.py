import folium
import os 

class Schedule:
    def __init__(self, coordinates, chargingStops, finalStop, tripTime, finalBatteryLevel, isSuccesful, tripStats):
        self.Coordinates = coordinates
        self.ChargingStops = chargingStops
        self.TripTime = tripTime
        self.FinalBatteryLevel = finalBatteryLevel
        self.IsSuccesful = isSuccesful
        self.FinalStop = finalStop
        self.TripStats = tripStats

    def Print(self):
        if self.IsSuccesful:
            print 'Trip Successful! \nTotal Time: {0} minutes ({1} time blocks) \n'.format(self.TripTime*15, self.TripTime)
                
            if self.ChargingStops != []:
                print 'Stop at the following locations: \n\n'

            for order, stop in enumerate(self.ChargingStops):
                print '{0}: {1} (stop {2}) for {3} minutes ({4} time blocks)'\
                    .format(order, stop.Name, stop.Order, stop.TimeAtStop*15, stop.TimeAtStop)

        else:
            print 'Trip failed after {0} minutes ({1} time blocks) at {2} (stop {3})'\
                .format(self.TripTime*15, self.TripTime, self.FinalStop.Name, self.FinalStop.Order)

        self.DrawMap()

    def DrawMap(self): 
        """
            Draw a route on an OSM map and display the charging points on top of it. 
        """   
        
        if self.Coordinates != []:
            # Create the map and add the line
            print('Drawing route')
            m = folium.Map(location=[41.9, -97.3], zoom_start=4)
            polyline = folium.PolyLine(locations=self.Coordinates, weight=5)
            m.add_child(polyline)

            for stop in self.ChargingStops:
                folium.Marker(location=[stop.Location.Latitude, stop.Location.Longitude], popup=stop.Name + '\n Stop for {0} mintues'.format(stop.TimeAtStop)).add_to(m)


            if not os.path.exists("temp"):
                os.mkdir('temp/')

            filepath = 'temp/map.html'
            m.save(filepath)
            #webbrowser.open(filepath)

            print 'Saved route to {0}'.format(filepath)
