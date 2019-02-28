from stat import Stat

import numpy as np

from schedule import Schedule
from schedule_stop import ScheduleStop

from ..environment import SimpleEnvironment


class Optimizer:
    def __init__(self):
        pass

    def ComputeExpectedValue(self, environment):
        NumberOfStops = environment.NumberOfStops
        MaxTripTime = environment.MaxTripTime
        MaxBattery = environment.MaxBattery
        ActionSpace = environment.ActionSpace
        Transitions = environment.Transitions
        values = np.zeros((NumberOfStops, MaxTripTime, MaxBattery))
        discount = 1.0
        iteration = 0

        while True:
            delta = 0
            valuesCopy = values.copy()
            iteration += 1
            print 'Iteration {0}'.format(iteration)

            for stop in range(NumberOfStops):
                for time in range(MaxTripTime):
                    for batteryLevel in range(MaxBattery):
                        actionSpace = ActionSpace[stop, time, batteryLevel]
                        expectedValues = []

                        for action in actionSpace:
                            reward = Transitions[stop, time, batteryLevel, action].Reward
                            nextState = Transitions[stop, time, batteryLevel, action].NextState
                            expectedValues.append(reward + discount * values[nextState.StopIndex,\
                                 nextState.TimeBlock, nextState.BatteryLevel])

                        if actionSpace == []:
                            continue

                        values[stop, time, batteryLevel] = np.max(expectedValues)

            delta = np.sum(np.fabs(valuesCopy - values))

            if(delta <= 0.1):
                break
        
        self.Values = values
        return self.Values

    def GetOptimalPolicy(self, values, environment):
        NumberOfStops = environment.NumberOfStops
        MaxTripTime = environment.MaxTripTime
        MaxBattery = environment.MaxBattery
        ActionSpace = environment.ActionSpace
        Transitions = environment.Transitions
        Values = values
        policy = np.zeros((NumberOfStops, MaxTripTime, MaxBattery)).astype(int)

        for stop in range(NumberOfStops - 1, -1, -1):
            for time in range(MaxTripTime - 1, -1, -1):
                for batteryLevel in range(MaxBattery):
                    actionSpace = ActionSpace[stop, time, batteryLevel]
                    expectedValues = []

                    for action in actionSpace:
                        reward = Transitions[stop, time, batteryLevel, action].Reward
                        nextState = Transitions[stop, time, batteryLevel, action].NextState
                        expectedValues.append(reward + Values[nextState.StopIndex, nextState.TimeBlock, nextState.BatteryLevel])

                    if actionSpace == []:
                        continue

                    policy[stop, time, batteryLevel] = int(np.argmax(expectedValues))

        self.Policy = policy
        return self.Policy

    def GetSchedule(self, policy, route, environment):
        totalReward = 0.0
        chargingStations = []
        tripStats = []
        tripTime = 0
        state = environment.Reset()
        tripStats.append(Stat(state, None))

        while True:

            actionToTake = policy[state.StopIndex, state.TimeBlock, state.BatteryLevel]

            nextState, reward, isDone = environment.Step(actionToTake)
            tripTime += (nextState.TimeBlock - tripTime)
            totalReward += reward

            if actionToTake == 1:
                if self.IsStopInList(nextState.StopIndex, chargingStations):
                    chargingStations[self.GetStopIndex(nextState.StopIndex, chargingStations)].TimeAtStop += 1
                else:
                    chargingStations.append(ScheduleStop(nextState.StopIndex, route.PossibleStops[nextState.StopIndex].Name, 1, route.PossibleStops[nextState.StopIndex].Location))
            
            state = nextState
            tripStats.append(Stat(state, actionToTake))

            if isDone:
                break       

        if nextState.StopIndex == environment.NumberOfStops - 1:
            return Schedule(route.Coordinates, chargingStations, route.PossibleStops[nextState.StopIndex], tripTime, nextState.BatteryLevel, True, tripStats)
        else:
            return Schedule(route.Coordinates, chargingStations, route.PossibleStops[nextState.StopIndex], tripTime, nextState.BatteryLevel, False, tripStats)

    def GetStopIndex(self, currentStop, chargingStations):
        for index, stop in enumerate(chargingStations):
            if currentStop == stop.Order:
                return index

        raise Exception("Stop not found!")
    def IsStopInList(self, currentStop, stopList):
        for stop in stopList:
            if currentStop == stop.Order:
                return True
        return False
