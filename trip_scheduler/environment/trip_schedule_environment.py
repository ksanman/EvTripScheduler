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
        # nextStopIndex = min(currentStopIndex + 1,  self.NumberOfStops - 1)
        # nextStop = self.Route[nextStopIndex]
        # nextTime = min(currentTime + nextStop.TimeFromPreviousStop, self.MaxTripTime - 1)
        # nextBattery = max(currentBatteryLevel - nextStop.EnergyExpended, 0)

        nextStopIndex = currentStopIndex + 1

        if nextStopIndex >= self.NumberOfStops: 
            return None, -100

        nextStop = self.Route[nextStopIndex]
        nextTime = currentTime + nextStop.TimeFromPreviousStop
        nextBattery = currentBatteryLevel - nextStop.EnergyExpended

        if nextTime >= self.MaxTripTime or nextBattery < 0:
            return None, -100

        reward = self.ComputeDrivingReward(nextStopIndex, nextTime, nextBattery)

        return State(nextStopIndex, nextTime, nextBattery), reward

    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the charging action. 
        """
        # charger = self.Route[currentStopIndex].ChargerConnection
        # nextTime = min(currentTime + 1,  self.MaxTripTime - 1)
        # deltaBattery =  RoundUp(self.Vehicle.Charge(currentBatteryLevel, charger))
        # nextBattery = min(currentBatteryLevel + deltaBattery, self.MaxBattery - 1)

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
        reward = self.ComputeTimeReward(stopIndex, timeBlock)
        if stopIndex ==  self.NumberOfStops - 1:
            if not self.HasFinalCharger:
                reward += 0 if batteryLevel > (float(self.MaxBattery) * 0.50) else -100
        else:
            reward += 0 if batteryLevel > (float(self.MaxBattery) * 0.20) else -10
            #0 if batteryLevel > (float(self.MaxBattery) * 0.50) \
            #    else -1 if batteryLevel > (float(self.MaxBattery) * 0.40)\
            #    else -2 if batteryLevel > (float(self.MaxBattery) * 0.30)\
            #    else -3 if batteryLevel > (float(self.MaxBattery) * 0.20) \
            #    else -150

        return reward

    def ComputeChargingReward(self, currentStopIndex, timeBlock, batteryLevel, batteryDelta, chargingPrice):
        timeReward = self.ComputeTimeReward(currentStopIndex, timeBlock)
        priceReward = -(0.13*(batteryDelta))
        chargingReward =  -10 if batteryLevel > (float(self.MaxBattery) * 0.90) \
                else 0 if batteryLevel > (float(self.MaxBattery) * 0.20)\
                else 1
        return timeReward + chargingReward + priceReward

    def ComputeTimeReward(self, stopIndex, time):
        if stopIndex != self.NumberOfStops - 1 and time == self.MaxTripTime:
            return -100

        return (self.ExpectedTripTime - time) if time > self.ExpectedTripTime else 1   

    def GetStopName(self, stopIndex):
        return self.Route[stopIndex].Name