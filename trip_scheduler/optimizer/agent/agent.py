class Agent(object):
    def __init__(self, environment):
        self.Environment = environment
        self.NumberOfStates = environment.NumberOfStates
        self.ActionSpace = environment.ActionSpace
        self.Transitions = environment.Transitions
        self.NumberOfStops = environment.NumberOfStops
        self.MaxTripTime = environment.MaxTripTime
        self.MaxBattery = environment.MaxBattery

    def FindBestSchedule(self):
        self.CalculateValueTable()
        self.FindOptimalPolicy()
        return self.GetSchedule()
