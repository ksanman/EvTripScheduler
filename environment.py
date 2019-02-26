import numpy as np
from transition import Transition
from decimal import Decimal, ROUND_HALF_UP
from visualize import Visualize


def RoundUp(value):
    return int(Decimal(value).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

class SimpleEnvironment:
    def __init__(self,trip):
        """ Creates a new Simple Ev Trip Schedule environment. 

            Keyword arguments:

            trip -- An object that contains a possible trip schedule, the expected trip time, and the vehicle used on the trip.
        """
        
        self.NumberOfStops = trip.NumberOfStops
        self.ExpectedTripTime = trip.ExpectedTripTime
        self.MaxTripTime = RoundUp(self.ExpectedTripTime * 1.25)
        self.MaxBattery = trip.BatteryCapacity
        self.HasFinalCharger = trip.HasDestinationCharger
        self.ActionSpace = np.array([[[[0] if stop == 0 \
            else [] if stop == self.NumberOfStops - 1 \
            else [0,1] \
            for _ in range(self.MaxBattery)] \
                for _ in range(self.MaxTripTime)] \
                    for stop in range(self.NumberOfStops)])

        self.Transitions = np.array([[[[None for _ in range(2)] \
            for _ in range(self.MaxBattery)] \
                for _ in range(self.MaxTripTime)] \
                    for _ in range(self.NumberOfStops)])
        self.PopulateTransitions()
        self.Visualizer = Visualize(self.NumberOfStops, self.MaxTripTime, self.MaxBattery, self.ExpectedTripTime)
        
    def PopulateTransitions(self):
        """ Populates the transition table for the given environment. 
        """
        for currentStopIndex in range(self.NumberOfStops):
            for currentTime in range(self.MaxTripTime):
                for currentBatteryLevel in range(self.MaxBattery):
                    actionSpace = self.ActionSpace[currentStopIndex, currentTime, currentBatteryLevel]
                    for action in actionSpace:
                        transition = self.GetTransition(currentStopIndex, currentTime, currentBatteryLevel, action)
                        self.Transitions[currentStopIndex, currentTime, currentBatteryLevel, action] = transition

    def GetTransition(self, currentStopIndex, currentTime, currentBatteryLevel, action):
        """ Gets the reward and next state for the given state and action. 
        """
        if action == 0:
            nextStopIndex, nextTime, nextBattery, reward = self.Drive(currentStopIndex, currentTime, currentBatteryLevel)
        elif action == 1:
            nextStopIndex, nextTime, nextBattery, reward = self.Charge(currentStopIndex, currentTime, currentBatteryLevel)
            
        isDone = True if nextStopIndex ==  self.NumberOfStops - 1 \
            else True if currentBatteryLevel == 0 \
                else True if currentTime ==  self.MaxTripTime - 1 \
                    else False

        return Transition(1.0, [nextStopIndex, nextTime, nextBattery], reward, isDone)
    
    def Drive(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the driving action. 
        """
        nextStopIndex = min(currentStopIndex + 1,  self.NumberOfStops - 1)
        nextTime = min(currentTime + 1, self.MaxTripTime - 1)
        nextBattery = max(currentBatteryLevel - 1, 0)
        reward = 1 if (self.ExpectedTripTime > nextTime) else -1
        if nextStopIndex ==  self.NumberOfStops - 1:
            if not self.HasFinalCharger:
                reward += 0 if currentBatteryLevel >  self.MaxBattery * 0.50 else -1
        else:
            reward += 0 if currentBatteryLevel >  self.MaxBattery * 0.20 else -1

        return (nextStopIndex, nextTime, nextBattery, reward)

    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        """ Computes the reward and next state for the charging action. 
        """
        nextStopIndex = currentStopIndex
        nextTime = min(currentTime + 1,  self.MaxTripTime - 1)
        nextBattery = min(currentBatteryLevel +  1,  self.MaxBattery - 1)
        reward = (self.ExpectedTripTime - nextTime) \
             + (-((0.13*nextBattery - currentBatteryLevel) \
                 + 0 + 0) if nextBattery < self.MaxBattery * .90 else -1)

        return (nextStopIndex, nextTime, nextBattery, reward)

    def ShowRewards(self):
        drivingRewards = np.zeros((self.NumberOfStops, self.MaxTripTime, self.MaxBattery))
        chargingRewards = np.zeros((self.NumberOfStops, self.MaxTripTime, self.MaxBattery))
        for stop in range(self.NumberOfStops):
            for time in range(self.MaxTripTime):
                for battery in range(self.MaxBattery):
                    drivingTransition =  self.Transitions[stop, time, battery, 0]
                    chargingTransition = self.Transitions[stop, time, battery, 1]
                    drivingRewards[stop, time, battery] = drivingTransition.Reward if drivingTransition else 0
                    chargingRewards[stop, time, battery] = drivingTransition.Reward if chargingTransition else 0

        self.Visualizer.VisualizeRewards(drivingRewards, chargingRewards)
        

if __name__ == '__main__':
    from trip import Trip

    trip = Trip(10, 10, 5, True)
    environment = SimpleEnvironment(trip)
    environment.ShowRewards()