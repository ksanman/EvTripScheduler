class Schedule:
    def __init__(self, polyline, chargingStops, totalTripTime, finalBatteryLevel):
        self.Polyline = polyline
        self.ChargingStops = chargingStops
        self.TotalTripTime = totalTripTime
        self.FinalBatteryLevel = finalBatteryLevel