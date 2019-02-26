from stop import Stop

class Start(Stop):
    def __init__(self, location):
        super(Start, self).__init__(location, 0, 0, 0)