from environment import Environment
from state import State
from ..utility import RoundUp

class EvTripScheduleEnvironment(Environment):
    def __init__(self,trip):
        """ Creates a new EvTripScheduleEnvironment Ev Trip Schedule environment. 

            Keyword arguments:

            trip -- An object that contains a possible trip schedule, the expected trip time, and the vehicle used on the trip.
        """
        self.Route = trip.Route.PossibleStops
        self.Vehicle = trip.Vehicle

        numberOfStops = len(self.Route)
        batteryCapacity = self.Vehicle.BatteryCapacity
        hasDestinationCharger = trip.HasDestinationCharger
        
        super(EvTripScheduleEnvironment, self).__init__(numberOfStops, trip.ExpectedTripTime, batteryCapacity, hasDestinationCharger)
    
    def Drive(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the driving action. 
        """
        nextStopIndex = currentStopIndex + 1

        if nextStopIndex >= self.NumberOfStops: 
            return None, -100

        nextStop = self.Route[nextStopIndex]
        nextTime = currentTime + nextStop.TimeFromPreviousStop 
        # Unlike charging, going downhill may fill the battery up. The car will simple stop charging but keep going.
        nextBattery = min(currentBatteryLevel - nextStop.EnergyExpended, self.MaxBattery - 1)

        if nextTime >= self.MaxTripTime:
            return None, -100
        if nextBattery <= 0:
            return None, -100

        reward = self.ComputeDrivingReward(nextStopIndex, nextTime, nextBattery)

        return State(nextStopIndex, nextTime, nextBattery), reward

    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the charging action. 
        """
        charger = self.Route[currentStopIndex].ChargerConnection
        nextTime = currentTime + 1
        deltaBattery =  RoundUp(self.Vehicle.Charge(currentBatteryLevel, charger))
        nextBattery = currentBatteryLevel + deltaBattery

        if nextTime >= self.MaxTripTime:
            return None, -100
        elif nextBattery >= self.MaxBattery:
            return None, -100

        reward = self.ComputeChargingReward(currentStopIndex, nextTime, nextBattery, deltaBattery, charger.Price)

        return State(currentStopIndex, nextTime, nextBattery), reward

    def ComputeDrivingReward(self, stopIndex, timeBlock, batteryLevel):
        reward = 0#self.ComputeTimeReward(stopIndex, timeBlock)
        if stopIndex ==  self.NumberOfStops - 1: # at the last stop
            if not self.HasFinalCharger: # Last stop doesn't have a charger
                reward += -1000 if batteryLevel < (float(self.MaxBattery) * 0.50) else 0
        else: # All other stops
            reward += 0 if batteryLevel > (float(self.MaxBattery) * 0.20) else -1000

        return reward

    def ComputeChargingReward(self, currentStopIndex, timeBlock, batteryLevel, batteryDelta, chargingPrice):
        timeReward = 0#self.ComputeTimeReward(currentStopIndex, timeBlock)
        priceReward = 0#-(0.13*(batteryDelta))
        chargingReward =  0 if batteryLevel > (float(self.MaxBattery) * 0.90) \
                else 5 if batteryLevel > (float(self.MaxBattery) * 0.25)\
                else 10
        return timeReward + chargingReward + priceReward

    def ComputeTimeReward(self, stopIndex, time):
        if stopIndex != self.NumberOfStops - 1: #not end
            if time == self.MaxTripTime:
                    return -100
            return 0 #got more time
        #end
        if time >= self.MaxTripTime:
             return -100
        return (self.ExpectedTripTime - time)   

    def GetStopName(self, stopIndex):
        return self.Route[stopIndex].Name