from environment import Environment
from state import State
from ..utility import RoundUp

class BatteryRewardOnlyEnvironment(Environment):
    def __init__(self,trip):
        """ Creates a new EvTripScheduleEnvironment Ev Trip Schedule environment. 

            Keyword arguments:

            trip -- An object that contains a possible trip schedule, the expected trip time, and the vehicle used on the trip.
        """
        self.Route = trip.Route.PossibleStops
        self.Vehicle = trip.Vehicle

        numberOfStops = len(self.Route)
        batteryCapacity = self.Vehicle.BatteryCapacity
        hasDestinationCharger = self.Route[-1].ChargerConnection is not None
        
        super(BatteryRewardOnlyEnvironment, self).__init__(numberOfStops, trip.ExpectedTripTime, batteryCapacity, hasDestinationCharger)
    
    def Drive(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the driving action. 
        """
        nextStopIndex = min(currentStopIndex + 1,  self.NumberOfStops - 1)
        nextStop = self.Route[nextStopIndex]
        nextTime = min(currentTime + nextStop.TimeFromPreviousStop, self.MaxTripTime - 1)
        nextBattery = max(currentBatteryLevel - nextStop.EnergyExpended, 0)
        reward = self.ComputeReward(nextTime, nextBattery)

        return State(nextStopIndex, nextTime, nextBattery), reward

    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the charging action. 
        """
        charger = self.Route[currentStopIndex].ChargerConnection
        nextTime = min(currentTime + 1,  self.MaxTripTime - 1)
        deltaBattery =  RoundUp(self.Vehicle.Charge(currentBatteryLevel, charger))
        nextBattery = min(currentBatteryLevel + deltaBattery, self.MaxBattery - 1)
        reward = self.ComputeReward(nextTime, nextBattery)

        return State(currentStopIndex, nextTime, nextBattery), reward

    def ComputeReward(self, timeBlock, batteryLevel):
        maxBattery = self.MaxBattery + 1
        timeReward = self.ComputeTimeReward(timeBlock)
        batteryReward = -2 if batteryLevel < maxBattery * 0.20 \
            else -1 if batteryLevel < maxBattery * 0.40 \
                else 0 if batteryLevel < maxBattery * 0.80 \
                    else 0 if batteryLevel < maxBattery * 0.90\
                        else 0

        return timeReward + batteryReward

    def ComputeTimeReward(self, time):
        return (self.ExpectedTripTime - time) * 1.5 if time > self.ExpectedTripTime else 0   

    def GetStopName(self, stopIndex):
        return self.Route[stopIndex].Name