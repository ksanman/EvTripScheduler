import numpy as np
from ..utility import RoundUp
from transition import Transition
import abc, six
from state import State

@six.add_metaclass(abc.ABCMeta)
class Environment():
    """ Base class for an EV Trip Scheduling Environment.
    """
    def __init__(self, numberOfStops, expectedTripTime, maxBattery, hasDestinationCharger):
        self.NumberOfStops = numberOfStops
        self.ExpectedTripTime = expectedTripTime
        self.MaxTripTime = RoundUp(self.ExpectedTripTime * 1.25)
        self.MaxBattery = maxBattery + 1
        self.NumberOfStates = self.NumberOfStops * self.MaxTripTime * self.MaxBattery
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

        self.TerminalRewards = np.array([[0 for time in range(self.MaxTripTime)] for batteryLevel in range(self.MaxBattery)])

        self.CalculateTerminalRewards()

        print 'Building Environment:\n\nNumber of Stops: {0} \nExpected Trip Time: {1} ({2} minutes) \nMax Trip Time: {3} ({4} minutes) \nMax Battery: {5}\nHas Charger at Destination: {6} \nTotal Number of States: {7}'\
            .format(self.NumberOfStops, self.ExpectedTripTime, self.ExpectedTripTime*15, self.MaxTripTime, self.MaxTripTime*15, self.MaxBattery-1, self.HasFinalCharger, self.NumberOfStates)

        self.PopulateTransitions()

    def CalculateTerminalRewards(self):
        for batteryLevel in range(self.MaxBattery):
            for time in range(self.MaxTripTime):
                reward = 0
                if not self.HasFinalCharger:
                    if batteryLevel == 0:
                        reward -= 100
                    if time == self.MaxTripTime - 1:
                        reward -= 100
                else:
                    if time == self.MaxTripTime - 1:
                        reward -= 100

                self.TerminalRewards[batteryLevel, time] = reward

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
            nextState, reward = self.Drive(currentStopIndex, currentTime, currentBatteryLevel)
        elif action == 1:
            nextState, reward = self.Charge(currentStopIndex, currentTime, currentBatteryLevel)
            
        #isDone = True if nextState.StopIndex ==  self.NumberOfStops - 1 \
          #  else True if nextState.BatteryLevel == 0 \
           #     else True if nextState.TimeBlock ==  self.MaxTripTime - 1 \
            #        else False
        isDone =  nextState is None or nextState.StopIndex ==  self.NumberOfStops - 1

        return Transition(1.0, nextState, reward, isDone)

    @abc.abstractmethod
    def Drive(self, currentStopIndex, currentTime, currentBatteryLevel):
        pass

    @abc.abstractmethod
    def Charge(self, currentStopIndex, currentTime, currentBatteryLevel):
        pass

    # @abc.abstractmethod
    # def ComputeDrivingReward(self, stop, timeBlock, batteryLevel):
    #     pass

    # @abc.abstractmethod
    # def ComputeChargingReward(self, timeBlock, batteryLevel, batteryDelta, chargingPrice):
    #     pass

    # @abc.abstractmethod
    # def ComputeTimeReward(self, time):
    #     pass

    @abc.abstractmethod
    def GetStopName(self, index):
        pass

    def Reset(self):
        self.State = State(0, 0, self.MaxBattery-1)
        #self.State = State(0, 0, 3)
        return self.State

    def Step(self, action):
        transition = self.Transitions[self.State.StopIndex, self.State.TimeBlock, self.State.BatteryLevel, action]
        self.State = transition.NextState
        return (self.State, transition.Reward, transition.IsDone)

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