from context import TripParameters, TripScheduler

# Logan to St George
parameters = TripParameters(28, 40, 'NissanLeaf', startPoint=['41.74027','-111.84251'], endPoint=['37.095169','-113.575974'], hasDestinationCharger=True)

scheduler = TripScheduler()
schedule = scheduler.Schedule(parameters)
schedule.Print()