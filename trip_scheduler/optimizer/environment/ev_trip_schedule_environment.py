from environment import Environment
from action_space import ActionSpace, StartingActionSpace, ChargingDecisionPointActionSpace, DestinationActionSpace
from state import State
from transition import Transition

import numpy as np

class EvTripScheduleEnvironment:
    def __init__(self, route, expectedTripTime, car):

        self.NumberOfStops = len(route)
        self.Route = route

        self.ExpectedTripTime = expectedTripTime
        self.MaxTripTime = expectedTripTime * .25

        self.MaxBattery = car.Battery.Capacity
        self.Car = car

        self.NumberOfStates = self.NumberOfStops * self.MaxTripTime * self.MaxBattery

        transitions, actionSpace = self.BuildEnvironment()

        super(EvTripScheduleEnvironment, self).__init__(self.NumberOfStates, transitions, actionSpace)

    def BuildActionSpace(self):
        actionSpace = np.array([[[ StartingActionSpace() if stop == 0 \
            else DestinationActionSpace() if stop == self.NumberOfStops - 1 \
                else ChargingDecisionPointActionSpace() for battery in range(self.MaxBattery)]\
             for tripTime in range(self.MaxTripTime)] \
                 for stop in range(self.NumberOfStops)])

        return actionSpace

    def BuildEnvironment(self):
        actionSpace = self.BuildActionSpace()
        transitions = np.zeros((self.NumberOfStops, self.MaxTripTime, self.MaxBattery, ActionSpace.Actions))

        for stop in range(self.NumberOfStops):
            for timeBlock in range(self.MaxTripTime):
                for batteryLevel in range(self.MaxBattery):
                    stateActionSpace = actionSpace[stop, timeBlock, batteryLevel]

                    for action in stateActionSpace:
                        if action == ActionSpace.Drive:
                            nextState, reward = self.ComputeDrivingTransition(stop, timeBlock, batteryLevel)
                        elif action == ActionSpace.Charge:
                            nextState, reward = self.ComputeChargingTransition(stop, timeBlock, batteryLevel)
                        
                        if nextState.StopStop == self.Stops - 1 \
                            or nextState.TimeBlock == self.MaxTime - 1\
                                or (nextState.BatteryLevel == 0 and action is not 1):
                            isDone = True


                        transitions[stop, timeBlock, batteryLevel, action] =  Transition(nextState, 1.0, reward, isDone)

    def ComputeDrivingTransition(self, stop, timeBlock, batteryLevel):
        nextStop = min(stop + 1, self.Stops - 1)
        location = self.Route[nextStop]

        nextTime = min(timeBlock + location.TimeFromPreviousLocation, self.MaxTime - 1)
        nextBattery = max(batteryLevel + location.EnergyExpended, 0)

        # Set the time reward
        reward = self.ComputeReward((nextTime, self.ExpectedTime), self.RewardFunctions.ComputeTimeReward)

        # If the new state is the terminal state
        if nextStop == self.Stops - 1:

            # If there is not a charger at the terminal state, set a reward for having a battery over 20%.
            if not self.IsDestinationCharger:
                reward += self.ComputeReward((nextBattery, self.MaxBattery - 1), self.RewardFunctions.ComputeRewardForDestinationWithoutCharger)
        else:
            # Set the reward for all other driving states
            reward += self.ComputeReward((nextBattery, self.MaxBattery - 1), self.RewardFunctions.ComputeBatteryRewardForDriving)

        return State(nextStop, nextTime, nextBattery), reward

    def ComputeChargingTransition(self, stop, timeBlock, batteryLevel):
        nextStop = stop
        nextTime = min(timeBlock + 1, self.MaxTime - 1)
        nextBattery = min(batteryLevel + self.Battery.Charge(nextTime - timeBlock, self.Route[stop].Load), self.MaxBattery - 1)

        # Set the time reward
        reward = self.ComputeReward((nextTime, self.ExpectedTime), self.RewardFunctions.ComputeTimeReward)
        # Set the charging reward. The reward is negative for staying too long at a charger and overcharging the car. 
        reward += self.ComputeReward((nextBattery, self.MaxBattery - 1, nextBattery - batteryLevel, self.Route[stop].DistanceFromIntersection), self.RewardFunctions.ComputeBatteryRewardForCharging)

        return State(nextStop, nextTime, nextBattery), reward

    def GetActionSpace(self, stop, timeBlock, batteryLevel):
        return self.ActionSpace[stop, timeBlock, batteryLevel]