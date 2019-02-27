import numpy as np
from ..utility import RoundUp
from transition import Transition
import abc, six

@six.add_metaclass(abc.ABCMeta)
class Environment():
    """ Base class for an EV Trip Scheduling Environment.
    """
    def __init__(self, numberOfStops, expectedTripTime, maxBattery, hasDestinationCharger):
        self.NumberOfStops = numberOfStops
        self.ExpectedTripTime = expectedTripTime
        self.MaxTripTime = RoundUp(self.ExpectedTripTime * 1.25)
        self.MaxBattery = maxBattery
        self.HasFinalCharger = hasDestinationCharger
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

    @abc.abstractmethod
    def Drive(self, currentStopIndex, currentTime, currentBatteryLevel):
        pass

    @abc.abstractmethod
    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        pass

    @abc.abstractmethod
    def ComputeDrivingReward(self, stop, timeBlock, batteryLevel):
        pass

    @abc.abstractmethod
    def ComputeChargingReward(self, timeBlock, batteryLevel, batteryDelta, chargingPrice):
        pass

    @abc.abstractmethod
    def ComputeTimeReward(self, time):
        pass

    def GetRewards(self):
        drivingRewards = np.zeros((self.NumberOfStops, self.MaxTripTime, self.MaxBattery))
        chargingRewards = np.zeros((self.NumberOfStops, self.MaxTripTime, self.MaxBattery))
        for stop in range(self.NumberOfStops):
            for time in range(self.MaxTripTime):
                for battery in range(self.MaxBattery):
                    drivingTransition =  self.Transitions[stop, time, battery, 0]
                    chargingTransition = self.Transitions[stop, time, battery, 1]
                    drivingRewards[stop, time, battery] = drivingTransition.Reward if drivingTransition else 0.0
                    chargingRewards[stop, time, battery] = chargingTransition.Reward if chargingTransition else 0.0

        return drivingRewards, chargingRewards