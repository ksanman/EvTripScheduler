class Vehicle:
    """ Base Class to model an electric vehicle.
    """
    KhwPerKm = 1

    def __init__(self, batteryCapacity):
        self.BatteryCapacity = batteryCapacity

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