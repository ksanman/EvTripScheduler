from vehicle import Vehicle

class SimpleVehicle(Vehicle, object):

    KhwPerKm = 1

    def __init__(self, batteryCapacity, timeBlockConstant):
        super(SimpleVehicle, self).__init__(batteryCapacity, timeBlockConstant)
        
    def Drive(self, roadSegment):
        """ 
            Returns the energy expended for driving the given road segment
        """

        return roadSegment.Distance * self.KhwPerKm

    def Charge(self, currentBatteryLevel, chargingConnection):
        """
            Returns the energy gained for charging a battery on for 15 minutes. 
            The current battery level is provided to give a better estimation.
        """
        return currentBatteryLevel + 1