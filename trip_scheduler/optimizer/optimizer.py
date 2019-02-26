class Optimizer:
    def __init__(self):
        pass

    def OptimizeTripSchedules(self, schedules):
        for schedule in schedules:
            self.OptimizeSchedule(schedule)

    def OptimizeSchedule(self, schedule):

        environment = Environment(schedule.PossibleStops, schedule.ExpectedTripTime, schedule.Car)

        optimizedSchedule = self.OptimizeTripPolicy(environment)

    def OptimizeTripPolicy(self, environment):
        
        agent = Agent(environment)
        schedule = agent.FindBestSchedule()
        return schedule
