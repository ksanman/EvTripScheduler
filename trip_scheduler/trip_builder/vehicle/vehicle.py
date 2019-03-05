import abc, six

@six.add_metaclass(abc.ABCMeta)
class Vehicle():
    """ Base Class to model an electric vehicle.
    """
    def __init__(self, batteryCapacity, timeBlockConstant):
        self.BatteryCapacity = batteryCapacity
        self.TimeBlockConstant = timeBlockConstant

    @abc.abstractmethod
    def Drive(self, roadSegment):
        """ 
            Returns the energy expended for driving the given road segment
        """
        pass

    @abc.abstractmethod
    def Charge(self, currentBatteryLevel, chargingConnection):
        """
            Returns the energy gained for charging a battery on for 15 minutes. 
            The current battery level is provided to give a better estimation.
        """
        pass