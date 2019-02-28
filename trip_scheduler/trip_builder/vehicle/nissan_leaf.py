from vehicle import Vehicle
from ...utility import RoundUp

class NissanLeaf(Vehicle):

    KhwPerKm = 4.5

    def __init__(self, batteryCapacity):
        self.StateOfChargeMap = [0,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35,37.5,40,42.5,45,47.5,50,52.5,55,57.5,60,62.5,65,67.5,70,72.5,75,77.5,80,82.5,90,90.5,91,91.5,92,92.5,93,93.5,94,94.5,95,95.5,96,96.5,97,97.5,98,98.5,100]
        super(NissanLeaf, self).__init__(batteryCapacity)

    def Drive(self, roadSegment):
        """ 
            Returns the energy expended for driving the given road segment
        """

        return roadSegment.Distance / self.KhwPerKm

    def Charge(self, currentBatteryLevel, chargingConnection=None):
        """
            Returns the energy gained for charging a battery on for 15 minutes. 
            The current battery level is provided to give a better estimation.
        """
        currentIndex = self.StateofChargeLookup(currentBatteryLevel)
        newIndex = min(currentIndex + 15, len(self.StateOfChargeMap)-1)
        return currentBatteryLevel + RoundUp(self.BatteryCapacity * self.StateOfChargeMap[newIndex] * 0.01)

    def StateofChargeLookup(self, currentBatteryLevel):
        for charge in range(1, len(self.StateOfChargeMap)):
            leftSideRange = self.StateOfChargeMap[charge - 1]
            rightSideRange = self.StateOfChargeMap[charge]

            if currentBatteryLevel >= leftSideRange and currentBatteryLevel < rightSideRange:
                return charge-1

        raise Exception('Invalid battery level!')
            
