from stat import Stat

import numpy as np

from schedule import Schedule
from schedule_stop import ScheduleStop

from ..environment import SimpleEnvironment
from ..action_space import ActionSpace


class Optimizer:
    def __init__(self, timeBlockConstant):
        self.TimeBlockConstant = timeBlockConstant

    def ComputeExpectedValue(self, environment):
        NumberOfStops = environment.NumberOfStops
        MaxTripTime = environment.MaxTripTime
        MaxBattery = environment.MaxBattery
        TerminalRewards = environment.TerminalRewards
        ActionSpace = environment.ActionSpace
        Transitions = environment.Transitions
        values = np.zeros((NumberOfStops, MaxTripTime, MaxBattery))
        discount = 1.0
        iteration = 0

        # Get the terminal reward
        for time in range(MaxTripTime):
            for batteryLevel in range(MaxBattery):
                values[NumberOfStops - 1, time, batteryLevel] = TerminalRewards[batteryLevel, time]

        while True:
            delta = 0
            valuesCopy = values.copy()
            iteration += 1
            print 'Iteration {0}'.format(iteration)

            for stop in range(NumberOfStops - 2, -1, -1):
                for time in range(MaxTripTime - 1, -1, -1):
                    for batteryLevel in range(MaxBattery):
                        actionSpace = ActionSpace[stop, time, batteryLevel]
                        expectedValues = []

                        for action in actionSpace:
                            reward = Transitions[stop, time, batteryLevel, action].Reward
                            nextState = Transitions[stop, time, batteryLevel, action].NextState

                            if nextState is None:
                                expectedValues.append(reward)
                            else:
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
        policy = np.zeros((NumberOfStops, MaxTripTime, MaxBattery)).astype(int)

        for stop in range(NumberOfStops):
            for time in range(MaxTripTime):
                for batteryLevel in range(MaxBattery):
                    actionSpace = ActionSpace[stop, time, batteryLevel]
                    expectedValues = []

                    for action in actionSpace:
                        reward = Transitions[stop, time, batteryLevel, action].Reward
                        nextState = Transitions[stop, time, batteryLevel, action].NextState

                        if nextState is None:
                            expectedValues.append(reward)
                        else:
                            expectedValues.append(reward + values[nextState.StopIndex,\
                                    nextState.TimeBlock, nextState.BatteryLevel])

                    if actionSpace == []:
                        continue

                    policy[stop, time, batteryLevel] = int(np.argmax(expectedValues))

        self.Policy = policy
        return self.Policy

    def GetSchedule(self, policy, trip, environment):
        totalReward = 0.0
        chargingStations = []
        tripStats = []
        tripTime = 0
        state = environment.Reset()
        tripStats.append(Stat(state, None))

        while True:

            actionToTake = policy[state.StopIndex, state.TimeBlock, state.BatteryLevel]

            nextState, reward, isDone = environment.Step(actionToTake)
            totalReward += reward

            if nextState is None:
                break

            tripTime += (nextState.TimeBlock - tripTime)
            

            if actionToTake == ActionSpace.Charge:
                if self.IsStopInList(nextState.StopIndex, chargingStations):
                    chargingStations[self.GetStopIndex(nextState.StopIndex, chargingStations)].TimeAtStop += 1
                else:
                    chargingStations.append(ScheduleStop(nextState.StopIndex, trip.Route.PossibleStops[nextState.StopIndex].Name, 1, trip.Route.PossibleStops[nextState.StopIndex].Location))
            
            state = nextState
            tripStats.append(Stat(state, actionToTake))

            if isDone:
                break       

        if nextState is not None and nextState.StopIndex == environment.NumberOfStops - 1:
            return Schedule(trip.Route.Coordinates, chargingStations, trip.Route.PossibleStops[nextState.StopIndex], tripTime, nextState.BatteryLevel, True, tripStats, self.TimeBlockConstant, trip.TripName)
        else:
            return Schedule(trip.Route.Coordinates, chargingStations, trip.Route.PossibleStops[state.StopIndex], tripTime, state.BatteryLevel, False, tripStats, self.TimeBlockConstant, trip.TripName)

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
