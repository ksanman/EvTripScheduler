from environment import Environment
from state import State

class SimpleEnvironment(Environment):
    def __init__(self,trip):
        """ Creates a new Simple Ev Trip Schedule environment. 

            Keyword arguments:

            trip -- An object that contains a possible trip schedule, the expected trip time, and the vehicle used on the trip.
        """
        
        super(SimpleEnvironment, self).__init__(trip.NumberOfStops, trip.ExpectedTripTime, trip.BatteryCapacity, trip.HasDestinationCharger)
    
    def Drive(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the driving action. 
        """
        nextStopIndex = min(currentStopIndex + 1,  self.NumberOfStops - 1)
        nextTime = min(currentTime + 1, self.MaxTripTime - 1)
        nextBattery = max(currentBatteryLevel - 1, 0)
        reward = self.ComputeDrivingReward(nextStopIndex, nextTime, nextBattery)

        return State(nextStopIndex, nextTime, nextBattery), reward

    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the charging action. 
        """
        nextStopIndex = currentStopIndex
        nextTime = min(currentTime + 1,  self.MaxTripTime - 1)
        nextBattery = min(currentBatteryLevel +  1,  self.MaxBattery - 1)
        reward = self.ComputeChargingReward(nextTime, nextBattery, nextBattery-currentBatteryLevel, 0.13)

        return State(nextStopIndex, nextTime, nextBattery), reward

    def ComputeDrivingReward(self, stop, timeBlock, batteryLevel):
        reward = self.ComputeTimeReward(timeBlock)
        if stop ==  self.NumberOfStops - 1:
            if not self.HasFinalCharger:
                reward += 0 if batteryLevel >  self.MaxBattery * 0.50 else -1
        else:
            reward += 0 if batteryLevel >  self.MaxBattery * 0.20 else -1

        return reward

    def ComputeChargingReward(self, timeBlock, batteryLevel, batteryDelta, chargingPrice):
        timeReward = self.ComputeTimeReward(timeBlock)
        chargingReward = -((0.13*(batteryDelta)) + 0 + 0) if batteryLevel < self.MaxBattery * .90 else -1
        return timeReward + chargingReward

    def ComputeTimeReward(self, time):
        return self.ExpectedTripTime - time if time > self.ExpectedTripTime else 0   

    def GetStopName(self, stopIndex):
        return str(stopIndex)