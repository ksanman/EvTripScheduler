class Transition:
    def __init__(self, nextState, probability, reward, isDone):
        self.NextState = nextState
        self.Probability = probability
        self.Reward = reward
        self.IsDone = isDone