class Schedule:
    def __init__(self, routePolyline, chargingStops, finalStop, tripTime, finalBatteryLevel, isSuccesful, tripStats):
        self.Polyline = routePolyline
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
        pass