from agent import Agent
import numpy as np

class ValueIterationAgent(Agent):
    def __init__(self, environment):
        return super(ValueIterationAgent, self).__init__(environment)

    def CalculateValueTable(self):
        self.V = np.zeros((self.NumberOfStops, self.MaxTripTime, self.MaxBattery))

        # Calculate the terminal values
        finalStop = self.NumberOfStops - 2

        for timeBlock in range(self.MaxTripTime - 1, -1, -1):
            for batteryLevel in range(self.MaxBattery):
                actionSpace = self.ActionSpace[finalStop, timeBlock, batteryLevel]
                for action in actionSpace:
                    possibleValues = []
                    nextState = self.Transitions[finalStop, timeBlock, batteryLevel, action].NextState
                    reward = self.Transitions[finalStop, timeBlock, batteryLevel, action].Reward
                    possibleValues.append(reward + self.V[nextState.Stop, nextState.TimeBlock, nextState.BatteryLevel])

                self.V[finalStop, timeBlock, batteryLevel] = max(possibleValues)

        # Calculate the rest of the values
        iteration = 0
        while True:
            print iteration

            delta = 0
            v_copy = self.V.copy()
            iteration += 1

            for stop in range(finalStop - 1, -1, -1):
                for time in range(self.MaxTripTime - 1, -1, -1):
                    for batteryLevel in range(self.MaxBattery):
                        possibleValues = []
                        for action in self.ActionSpace[stop, time, batteryLevel]:
                            nextState = self.Transitions[stop, time, batteryLevel, action].NextState
                            reward = self.Transitions[stop, time, batteryLevel, action].Reward
                            possibleValues.append(reward + self.Discount * self.V[nextState.Stop, nextState.TimeBlock, nextState.BatteryLevel])
                
                        if possibleValues == []:
                            continue

                        self.V[stop, time, batteryLevel] = np.max(possibleValues)

            delta = np.sum(np.fabs(v_copy - self.V))

            if(delta <= 0.1):
                break

