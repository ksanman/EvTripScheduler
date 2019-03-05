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
        nextStopIndex = currentStopIndex + 1
        nextTime = currentTime + 1
        nextBattery = currentBatteryLevel - 1

        if nextStopIndex >= self.NumberOfStops or nextTime >= self.MaxTripTime or nextBattery < 0:
            return None, -100

        reward = self.ComputeDrivingReward(nextStopIndex, nextTime, nextBattery)

        return State(nextStopIndex, nextTime, nextBattery), reward

    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the charging action. 
        """
        nextStopIndex = currentStopIndex
        nextTime = currentTime + 1
        nextBattery = currentBatteryLevel +  1

        if nextTime >= self.MaxTripTime or nextBattery >= self.MaxBattery:
            return None, -100

        reward = self.ComputeChargingReward(nextStopIndex, nextTime, nextBattery, nextBattery-currentBatteryLevel, 0.13)

        return State(nextStopIndex, nextTime, nextBattery), reward

    def ComputeDrivingReward(self, stop, timeBlock, batteryLevel):
        reward = self.ComputeTimeReward(timeBlock, stop)
        if stop ==  self.NumberOfStops - 1:
            if not self.HasFinalCharger:
                reward += 0 if batteryLevel >  self.MaxBattery * 0.50 else -1
        else:
            reward += 0 if batteryLevel >  self.MaxBattery * 0.20 else -1

        return reward

    def ComputeChargingReward(self,stopIndex, timeBlock, batteryLevel, batteryDelta, chargingPrice):
        timeReward = self.ComputeTimeReward(timeBlock,stopIndex)
        chargingReward = -((0.13*(batteryDelta)) + 0 + 0) if batteryLevel < self.MaxBattery * .90 else -1
        return timeReward + chargingReward

    def ComputeTimeReward(self, time, stopIndex):
        if stopIndex != self.NumberOfStops -1 and time == self.MaxTripTime - 1:
            return -100
        return self.ExpectedTripTime - time if time > self.ExpectedTripTime else 0   

    def GetStopName(self, stopIndex):
        return str(stopIndex)