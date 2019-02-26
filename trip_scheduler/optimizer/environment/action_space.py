class ActionSpace(object):
    Drive = 0
    Charge = 1
    Actions = 2

    def __init__(self, actions):
        self.Actions = actions

class StartingActionSpace(ActionSpace):
    def __init__(self, actions):
        return super(StartingActionSpace, self).__init__([self.Drive])

class DestinationActionSpace(ActionSpace):
    def __init__(self, actions):
        return super(DestinationActionSpace, self).__init__([])

class ChargingDecisionPointActionSpace(ActionSpace):
    def __init__(self, actions):
        return super(ChargingDecisionPointActionSpace, self).__init__([self.Drive, self.Charge])