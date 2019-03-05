from vehicle import Vehicle
from ...utility import RoundUp

class NissanLeaf(Vehicle):

    KhwPerKm = 4.5

    def __init__(self, batteryCapacity, timeBlockConstant):
        super(NissanLeaf, self).__init__(batteryCapacity, timeBlockConstant)

    def Drive(self, roadSegment):
        """ 
            Returns the energy expended for driving the given road segment
        """

        return roadSegment.Distance / self.KhwPerKm

    def Charge(self, currentBatteryLevel, chargingConnection):
        """
            Returns the energy gained for charging a battery on for 15 minutes. 
            The current battery level is provided to give a better estimation.
        """
        hoursCharging = (float(self.TimeBlockConstant)/60.0)

        if currentBatteryLevel < self.BatteryCapacity * 0.70:
            
            charge = float(chargingConnection.Power) * hoursCharging
            return charge
        else:
            batteryPercentage = float(currentBatteryLevel)/float(self.BatteryCapacity) * 100.0

            # Curve dropping the charge rate to zero once the battery reaches 80%
            factor = float(chargingConnection.Power)/pow(70-100, 2)

            # deltaE = a(x-100)^2
            power = (factor) * pow(batteryPercentage - 100, 2)
            return power * hoursCharging