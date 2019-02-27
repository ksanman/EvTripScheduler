from environment import SimpleEnvironment
import numpy as np

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
                            nextStop, nextTime, nextBattery = Transitions[stop, time, batteryLevel, action].NextState
                            expectedValues.append(reward + discount * values[nextStop, nextTime, nextBattery])

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
        policy = np.zeros((NumberOfStops, MaxTripTime, MaxBattery))

        for stop in range(NumberOfStops - 1, -1, -1):
            for time in range(MaxTripTime - 1, -1, -1):
                for batteryLevel in range(MaxBattery):
                    actionSpace = ActionSpace[stop, time, batteryLevel]
                    expectedValues = []

                    for action in actionSpace:
                        reward = Transitions[stop, time, batteryLevel, action].Reward
                        nextStop, nextTime, nextBattery = Transitions[stop, time, batteryLevel, action].NextState
                        expectedValues.append(reward + Values[nextStop, nextTime, nextBattery])

                    if actionSpace == []:
                        continue

                    policy[stop, time, batteryLevel] = np.argmax(expectedValues)

        self.Policy = policy
        return self.Policy

    def GetSchedule(self, policy, environment):
        pass