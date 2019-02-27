class Transition:
    def __init__(self, probability, nextState, reward, isDone):
        self.Probability = probability
        self.NextState = nextState
        self.Reward = reward
        self.IsDone = isDone